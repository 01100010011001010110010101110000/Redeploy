import logging
import os

from redeploy import Redeployer

if __name__ == "__main__":
    logger = logging.getLogger('script')
    logger.setLevel(os.environ.get('LOG_LEVEL', 'INFO'))
    logger.addHandler(logging.StreamHandler())

    to_redeploy = os.environ.get("DEPLOYMENT", "")
    if len(to_redeploy) == 0:
        logger.warning("No deployment specified, exiting")
        exit(0)
    namespace = os.environ.get("NAMESPACE", 'default')
    redeployer = Redeployer(to_redeploy, namespace)
    redeployer.redeploy()
