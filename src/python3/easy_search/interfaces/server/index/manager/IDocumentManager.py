from abc import ABCMeta, abstractmethod
from typing import Type, Iterator

from easy_search.interfaces.base.communication.response.BaseResponse import BaseResponse
from easy_search.interfaces.server.index.communication.common import IndexDocument
from easy_search.interfaces.server.index.communication.request.SearchQuery import SearchQuery
from easy_search.interfaces.server.index.communication.response.DocumentResponse import DocumentResponse
from easy_search.interfaces.server.index.communication.response.SearchResult import SearchResult


class IDocumentManager:
    __metaclass__ = ABCMeta
    index_object_type: Type[object] = IndexDocument

    @abstractmethod
    def add(self, document: IndexDocument) -> BaseResponse: raise NotImplementedError

    @abstractmethod
    def delete(self, unique_id: str) -> BaseResponse: raise NotImplementedError

    @abstractmethod
    def get(self, unique_id: str) -> DocumentResponse: raise NotImplementedError

    @abstractmethod
    def search(self, query: SearchQuery) -> SearchResult: raise NotImplementedError
