from collections.abc import Callable
from typing import Any

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from kwality.utils.logger import get_logger

logger = get_logger(__name__)


class Scheduler:
    """
    Thin wrapper around APScheduler for
    running jobs on cron timings.
    """

    def __init__(self, timezone: str = "UTC") -> None:
        self._scheduler = BackgroundScheduler(timezone=timezone)

    def add_job(
        self,
        func: Callable[..., Any],
        cron: str,
        job_id: str | None = None,
        args: tuple[Any, ...] = (),
        kwargs: dict[str, Any] | None = None,
    ) -> None:
        """
        Schedule func using a crontab expression
        e.g. '*/5 * * * *'.
        """
        trigger = CronTrigger.from_crontab(cron, timezone=self._scheduler.timezone)
        self._scheduler.add_job(
            func,
            trigger,
            id=job_id,
            args=args,
            kwargs=kwargs,
            replace_existing=job_id is not None,
            coalesce=True,
            max_instances=1,
            misfire_grace_time=60,
        )
        logger.info(
            "Scheduled job %s with cron timing '%s'", job_id or func.__name__, cron
        )

    def start(self) -> None:
        self._scheduler.start()
        logger.info("Scheduler started")

    def shutdown(self) -> None:
        if self._scheduler.running:
            self._scheduler.shutdown()
            logger.info("Scheduler stopped")
