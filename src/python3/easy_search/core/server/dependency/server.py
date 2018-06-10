from easy_search.core.server.job.manager.JobScheduler import JobScheduler
from easy_search.interfaces.server.job.data.ISearchEngineContext import ISearchEngineContext
from easy_search.interfaces.server.job.manager import IJobScheduler


def job_scheduler(context: ISearchEngineContext) -> IJobScheduler:
    return JobScheduler(context)
