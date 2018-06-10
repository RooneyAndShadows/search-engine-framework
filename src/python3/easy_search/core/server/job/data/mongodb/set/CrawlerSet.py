from datetime import datetime
from uuid import UUID

from pymongo.collection import Collection

from .base.BaseSet import BaseSet
from easy_search.interfaces.server.job.data.entity.Crawler import Crawler as CrawlerDTO
from easy_search.interfaces.server.job.data.exception.EntityNotFoundException import EntityNotFoundException
from easy_search.interfaces.server.job.data.set.ICrawlerSet import ICrawlerSet


class CrawlerSet(BaseSet, ICrawlerSet):
    def get_collection(self) -> Collection:
        return self.database.crawlers

    def covert(self, entity) -> CrawlerDTO:
        crawler = CrawlerDTO(entity["crawler_id"], entity["allowed_ip"], entity["date_added"])
        if entity["last_call"] is not None:
            crawler.set_last_call_date(entity["last_call"])
        return crawler

    def register_call(self, crawler_id: UUID) -> None:
        self.get_collection().find_one_and_update({"crawler_id": crawler_id.__str__()},
                                                  {"$set": {"last_call": datetime.now()}})

    def exists(self, crawler_id: UUID) -> bool:
        crawler_list = self.get_collection().find({"crawler_id": crawler_id.__str__()})
        return crawler_list.count() > 0

    def get(self, crawler_id: UUID) -> CrawlerDTO:
        entity = self.get_collection().find_one({"crawler_id": crawler_id.__str__()})
        if entity is None:
            raise EntityNotFoundException("Crawler with given id does not exist!")
        return self.covert(entity)
