from .decorators import task
from core.logger import logger
from core.helpers import timer
import time


@task
def test_task(*args, **kwargs):
    logger.info('Работает')
    time.sleep(40)
    logger.info(args)
    logger.info(kwargs)

@timer
def test_job():
    with open('/app/test.txt', 'w') as f:
        f.write('1')
    print('test task complited')
    time.sleep(20)