import datetime
from uuid import UUID

from ....enum.JobType import JobType


class JobData(object):
    def __init__(self, job_type: JobType, target: str, locked: bool, creator_crawler_id: UUID) -> None:
        self.type = job_type
        self.target = target
        self.locked = locked
        self.creator_id = creator_crawler_id
        self.executor_id = None
        self.date_executed = None

    def set_executor_crawler_id(self, crawler_id: UUID, date_executed: datetime) -> None:
        self.executor_id = crawler_id
        self.date_executed = date_executed
