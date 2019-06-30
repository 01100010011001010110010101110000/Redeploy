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

    def __init__(self, deployment, namespace):
        kubernetes.config.load_incluster_config()
        self.logger.setLevel(os.environ.get('LOG_LEVEL', 'INFO'))
        self.logger.addHandler(logging.StreamHandler())
        self.deployment = deployment
        self.namespace = namespace
        self.api_instance = kubernetes.client.AppsV1Api()

    @staticmethod
    def apply_restart_annotation(deployment, restart_time):
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
