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

    def redeploy(self):
        try:
            deployment = self.api_instance.read_namespaced_deployment(self.deployment, self.namespace)
            if deployment.spec.template.metadata.annotations is not None:
                deployment.spec.template.metadata.annotations['restartedAt'] = datetime.datetime.utcnow().isoformat()
            else:
                deployment.spec.template.metadata.annotations = {
                    'restartedAt': datetime.datetime.utcnow().isoformat()
                }
            self.api_instance.patch_namespaced_deployment(self.deployment, self.namespace, deployment)
        except ApiException as e:
            logging.error(f"Error while redeploying {self.namespace}/{self.deployment}: {e.reason}")
            exit(1)
