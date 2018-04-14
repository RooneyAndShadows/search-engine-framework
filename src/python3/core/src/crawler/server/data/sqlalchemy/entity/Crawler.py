import uuid

from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import String, TIMESTAMP

from core.src.crawler.server.data.sqlalchemy.custom_types.Guid import GUID
from core.src.crawler.server.data.sqlalchemy.entity.Base import Base


class Crawler(Base):
    __tablename__ = 'crawlers'

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    allowed_ip = Column(String, nullable=False)
    date_added = Column(TIMESTAMP, nullable=False)
    last_call = Column(TIMESTAMP)

    def __repr__(self):
        return "<Crawler(allowed_ip='%s', date_added='%s', last_call='%s')>" % (
                          self.allowed_ip, self.date_added, self.last_call)
