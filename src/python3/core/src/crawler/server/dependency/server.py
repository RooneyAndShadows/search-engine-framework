from core.src.crawler.server.manager.JobScheduler import JobScheduler
from interfaces.src.crawler.server.data.ISearchEngineContext import ISearchEngineContext
from interfaces.src.crawler.server.manager.IJobScheduler import IJobScheduler


def job_scheduler(context: ISearchEngineContext) -> IJobScheduler:
    return JobScheduler(context)
