from datetime import datetime, timedelta
from uuid import UUID

from easy_search.interfaces.server.job.data.ISearchEngineContext import ISearchEngineContext
from easy_search.interfaces.server.job.data.data.JobData import JobData
from easy_search.interfaces.server.job.repository.IRepository import IRepository


class Repository(IRepository):

    def __init__(self, context: ISearchEngineContext) -> None:
        self.context = context

    def finish_job(self, job_id: UUID, crawler_id: UUID) -> None:
        job = self.context.job_set().get(job_id)
        data = JobData(job.type, job.target, job.locked, job.creator_id, job.plugin_type, job.repeat)
        data.set_executor_crawler_id(crawler_id, datetime.now())
        data.locked = False
        if data.repeat is not None:
            data.repeat_after = data.date_executed + timedelta(seconds=data.repeat)
        self.context.job_set().edit(job_id, data)


