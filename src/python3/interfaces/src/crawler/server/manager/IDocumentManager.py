from abc import ABCMeta, abstractmethod

from interfaces.src.crawler.communication.response.BaseResponse import BaseResponse
from interfaces.src.crawler.index.IndexDocument import IndexDocument


class IDocumentManager:
    __metaclass__ = ABCMeta

    @abstractmethod
    def add(self, document: IndexDocument) -> BaseResponse: raise NotImplementedError

    @abstractmethod
    def delete(self, unique_id: str) -> BaseResponse: raise NotImplementedError
