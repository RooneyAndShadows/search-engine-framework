import datetime
from uuid import UUID


class Crawler(object):
    def __init__(self, crawler_id: UUID, allowed_ip_list: list, date_added: datetime) -> None:
        self.crawler_id = crawler_id
        self.allowed_ip_list = allowed_ip_list
        self.date_added = date_added
        self.last_call_date = None

    def set_last_call_date(self, date: datetime) -> None:
        self.last_call_date = date
