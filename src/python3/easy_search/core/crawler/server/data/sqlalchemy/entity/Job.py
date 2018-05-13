import uuid

from sqlalchemy import Integer, Boolean
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import String, TIMESTAMP

from ..custom_types.Guid import GUID
from .Base import Base


class Job(Base):
    __tablename__ = 'jobs'

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    type = Column(Integer, nullable=False)
    url = Column(String, nullable=False)
    hash = Column(String, nullable=False)
    locked = Column(Boolean, nullable=False)
    crawler_id = Column(GUID, nullable=False)
    done_by = Column(GUID)
    date_added = Column(TIMESTAMP, nullable=False)
    date_done = Column(TIMESTAMP)

    def __repr__(self):
        return "<Job(id='%s' type='%s', url='%s', hash='%s', " \
               "locked='%s', crawler_id='%s', done_by='%s', date_done='%s', date_added='%s')>" % (
                          self.id, self.type, self.url, self.hash, self.locked, self.crawler_id, self.done_by,
                          self.date_done, self.date_added)
