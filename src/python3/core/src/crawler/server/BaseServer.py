from abc import ABCMeta

from core.src.crawler.server.dependency.server import job_scheduler
from interfaces.src.crawler.server.data.ISearchEngineContext import ISearchEngineContext


class BaseServer:
    __metaclass__ = ABCMeta

    def __init__(self, context: ISearchEngineContext) -> None:
        self.job_scheduler = job_scheduler(context)




