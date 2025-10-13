from .decorators import task
from core.logger import logger
import time


@task
def test_task(*args, **kwargs):
    logger.info('Работает')
    time.sleep(40)
    logger.info(args)
    logger.info(kwargs)