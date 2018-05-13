from abc import ABCMeta, abstractmethod

from ...communication.response.BaseResponse import BaseResponse
from ...index.IndexDocument import IndexDocument


class IDocumentManager:
    __metaclass__ = ABCMeta

    @abstractmethod
    def add(self, document: IndexDocument) -> BaseResponse: raise NotImplementedError

    @abstractmethod
    def delete(self, unique_id: str) -> BaseResponse: raise NotImplementedError
