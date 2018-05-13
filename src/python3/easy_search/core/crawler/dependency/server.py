from ..server.manager.JobScheduler import JobScheduler
from easy_search.interfaces.crawler.server.data.ISearchEngineContext import ISearchEngineContext
from easy_search.interfaces.crawler.server.manager.IJobScheduler import IJobScheduler


def job_scheduler(context: ISearchEngineContext) -> IJobScheduler:
    return JobScheduler(context)
