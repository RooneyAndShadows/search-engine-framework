from typing import TypeVar, Generic

from easy_search.interfaces.server.index.communication.common import IndexDocument
from easy_search.interfaces.base.communication.response.BaseResponse import BaseResponse


class SearchResult(BaseResponse):
    def __init__(self, is_successful: bool = False):
        super().__init__(is_successful)
        self.result_list = []

    def add_result(self, result: IndexDocument) -> None:
        self.result_list.append(result)
