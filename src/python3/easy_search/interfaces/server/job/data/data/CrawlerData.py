import datetime


class CrawlerData(object):
    def __init__(self, allowed_ip_list: list) -> None:
        self.allowed_ip_list = allowed_ip_list
        self.last_call_date = None

    def set_last_call_date(self, date: datetime) -> None:
        self.last_call_date = date
