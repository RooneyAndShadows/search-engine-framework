from typing import List

from .common.SearchCriteria import SearchCriteria
from .common.RangeCriteria import RangeCriteria


class SearchQuery:
    def __init__(self, searchCriteria: List[SearchCriteria] = [], rangeCriteria: List[RangeCriteria] = [],
                 orderCriteria: dict = {}, page: int = 0, items: int = 10) -> None:
        super().__init__()
        self.searchCriteria = searchCriteria
        self.rangeCriteria = rangeCriteria
        self.orderCriteria = orderCriteria
        self.page = page
        self.items = items

    def add_search_criteria(self, criteria: SearchCriteria):
        self.searchCriteria.append(criteria)

    def add_range_criteria(self, criteria: RangeCriteria):
        self.rangeCriteria.append(criteria)

    def add_order_criteria(self, field: str, order_type: str):
        self.orderCriteria[field] = order_type
