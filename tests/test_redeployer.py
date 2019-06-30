import datetime
from unittest import TestCase

import kubernetes.client
import kubernetes.config

from redeploy import Redeployer


class TestRedeployer(TestCase):
    docker_coredns_deployment = 'coredns'

    def test_apply_restart_annotation(self):
        kubernetes.config.load_kube_config(context='docker-desktop')
        restart_time = datetime.datetime.utcnow().isoformat()
        api_instance = kubernetes.client.AppsV1Api()
        deployment = api_instance.read_namespaced_deployment(self.docker_coredns_deployment, 'kube-system')
        deployment = Redeployer.apply_restart_annotation(deployment, restart_time)
        self.assertEqual(deployment.spec.template.metadata.annotations['restartedAt'], restart_time)