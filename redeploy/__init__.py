import datetime
import logging
import os

import kubernetes.client
import kubernetes.config

from kubernetes.client.rest import ApiException


class Redeployer():
    deployment = ""
    namespace = ""
    api_instance = None

    logger = logging.getLogger('redeployer')

    def __init__(self, deployment: str, namespace: str) -> None:
        """
        Initializes the k8s client with the default token injected into a pod
        :param deployment: The name of the deployment to restart
        :param namespace: The namespace of the deployment
        """
        kubernetes.config.load_incluster_config()
        self.logger.setLevel(os.environ.get('LOG_LEVEL', 'INFO'))
        self.logger.addHandler(logging.StreamHandler())
        self.deployment = deployment
        self.namespace = namespace
        self.api_instance = kubernetes.client.AppsV1Api()

    @staticmethod
    def apply_restart_annotation(deployment: kubernetes.client.models.AppsV1beta1Deployment, restart_time: str) -> kubernetes.client.models.AppsV1beta1Deployment:
        """
        Adds a `restartedAt` field to the deployment template's annotations to trigger a rolling restart
        :param deployment: The deployment object to restart
        :param restart_time: The restart time to update on the deployment metadata
        :return: The updated deployment object
        """
        if deployment.spec.template.metadata.annotations is not None:
            deployment.spec.template.metadata.annotations['restartedAt'] = restart_time
        else:
            deployment.spec.template.metadata.annotations = {
                'restartedAt': restart_time
            }
        return deployment

    def redeploy(self):
        try:
            deployment = self.api_instance.read_namespaced_deployment(self.deployment, self.namespace)
            deployment = self.apply_restart_annotation(deployment, datetime.datetime.utcnow().isoformat())
            self.api_instance.patch_namespaced_deployment(self.deployment, self.namespace, deployment)
        except ApiException as e:
            logging.error(f"Error while redeploying {self.namespace}/{self.deployment}: {e.reason}")
            exit(1)
