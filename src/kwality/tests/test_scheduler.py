from __future__ import annotations

from kwality.utils.scheduler import Scheduler


def test_scheduler_add_job_registers_callable():
    scheduler = Scheduler(timezone="UTC")

    def sample_job() -> None:
        return None

    scheduler.add_job(sample_job, "*/5 * * * *", job_id="sample-job")

    jobs = scheduler._scheduler.get_jobs()
    assert len(jobs) == 1
    assert jobs[0].id == "sample-job"
    assert jobs[0].func == sample_job

    scheduler.shutdown()


def test_scheduler_uses_expected_trigger_configuration():
    scheduler = Scheduler(timezone="UTC")

    def sample_job() -> None:
        return None

    scheduler.add_job(sample_job, "0 9 * * *", job_id="daily-job")

    job = scheduler._scheduler.get_jobs()[0]

    assert job.trigger is not None
    assert job.coalesce is True
    assert job.max_instances == 1
    assert job.misfire_grace_time == 60

    scheduler.shutdown()


def test_scheduler_start_then_shutdown_runs_cleanly():
    scheduler = Scheduler(timezone="UTC")

    def sample_job() -> None:
        return None

    scheduler.add_job(sample_job, "*/15 * * * *", job_id="start-stop-job")
    scheduler.start()
    assert scheduler._scheduler.running is True

    scheduler.shutdown()
    assert scheduler._scheduler.running is False
