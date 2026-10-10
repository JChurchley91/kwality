import time

from dags.raw_tests import run_raw_tests
from kwality.utils.logger import get_logger
from kwality.utils.scheduler import Scheduler

logger = get_logger(__name__)

try:
    logger.info("Initializing Kwality.")
    scheduler = Scheduler()
    scheduler.add_job(run_raw_tests, "* * * * *", job_id="raw_tests")
    scheduler.start()
except Exception as e:
    logger.error("Failed to start scheduler: %s", e)
    raise

try:
    while True:
        time.sleep(1)
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
