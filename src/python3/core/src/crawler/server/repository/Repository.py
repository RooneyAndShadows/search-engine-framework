from datetime import datetime
from uuid import UUID

from interfaces.src.crawler.server.data.ISearchEngineContext import ISearchEngineContext
from interfaces.src.crawler.server.data.data.JobData import JobData
from interfaces.src.crawler.server.repository.IRepository import IRepository


class Repository(IRepository):

    def __init__(self, context: ISearchEngineContext) -> None:
        self.context = context

    def finish_job(self, job_id: UUID, crawler_id: UUID) -> None:
        job = self.context.job_set().get(job_id)
        data = JobData(job.type, job.target, job.locked, job.creator_id)
        data.set_executor_crawler_id(crawler_id, datetime.now())
        self.context.job_set().edit(job_id, data)


