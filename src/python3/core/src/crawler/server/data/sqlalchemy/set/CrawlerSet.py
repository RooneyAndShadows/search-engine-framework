from datetime import datetime
from uuid import UUID

from core.src.crawler.server.data.sqlalchemy.entity.Crawler import Crawler
from core.src.crawler.server.data.sqlalchemy.set.base.BaseSet import BaseSet
from interfaces.src.crawler.server.data.entity.Crawler import Crawler as CrawlerDTO
from interfaces.src.crawler.server.data.set.ICrawlerSet import ICrawlerSet


class CrawlerSet(BaseSet, ICrawlerSet):
    def covert(self, entity: Crawler) -> CrawlerDTO:
        crawler = CrawlerDTO(entity.id, entity.allowed_ip.split('|'), entity.date_added)
        if entity.last_call is not None:
            crawler.set_last_call_date(entity.last_call)
        return entity

    def register_call(self, crawler_id: UUID) -> None:
        query = self.session.query(Crawler)
        crawler = query.filter(Crawler.id == crawler_id).one()
        crawler.last_call = datetime.now()

    def exists(self, crawler_id: UUID) -> bool:
        query = self.session.query(Crawler)
        return query\
            .filter(Crawler.id == crawler_id)\
            .count() > 0

    def get(self, crawler_id: UUID) -> CrawlerDTO:
        query = self.session.query(Crawler)
        entity = query.filter(Crawler.id == crawler_id).one()
        return self.covert(entity)
