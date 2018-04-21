from pymongo import MongoClient

from core.src.crawler.server.data.mongodb.set.CrawlerSet import CrawlerSet
from core.src.crawler.server.data.mongodb.set.JobSet import JobSet
from interfaces.src.crawler.server.data.ISearchEngineContext import ISearchEngineContext
from interfaces.src.crawler.server.data.set.ICrawlerSet import ICrawlerSet
from interfaces.src.crawler.server.data.set.IJobSet import IJobSet


class SearchEngineContext(ISearchEngineContext):

    def job_set(self) -> IJobSet:
        return self.job_set_instance

    def crawler_set(self) -> ICrawlerSet:
        return self.crawler_set_instance

    def save(self) -> None:
        pass

    def start_transaction(self) -> None:
        pass

    def rollback(self) -> None:
        pass

    def commit(self) -> None:
        pass

    def __init__(self, database_connection: str, db_name: str):
        self.client = MongoClient(database_connection)
        self.database = self.client[db_name]
        self.crawler_set_instance = CrawlerSet(self.database)
        self.job_set_instance = JobSet(self.database)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.client.close()
