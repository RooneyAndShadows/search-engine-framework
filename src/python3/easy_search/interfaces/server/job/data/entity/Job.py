import datetime
from uuid import UUID

from easy_search.interfaces.base.enum.JobType import JobType


class Job(object):
    def __init__(self, job_id: UUID, job_type: JobType, target: str, unique_hash: str, locked: bool,
                 date_added: datetime, creator_crawler_id: UUID, plugin: str):
        self.job_id = job_id
        self.type = job_type
        self.target = target
        self.plugin_type = plugin
        self.hash = unique_hash
        self.locked = locked
        self.date_added = date_added
        self.creator_id = creator_crawler_id
        self.executor_id = None
        self.date_executed = None

    def set_executor_crawler_id(self, crawler_id: UUID, date_executed: datetime):
        self.executor_id = crawler_id
        self.date_executed = date_executed
