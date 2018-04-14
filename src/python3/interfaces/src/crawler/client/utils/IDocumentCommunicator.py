from abc import ABC, abstractmethod

from interfaces.src.crawler.index.IndexDocument import IndexDocument


class IDocumentCommunicator(object):
    __metaclass__ = ABC

    @abstractmethod
    def add_document(self, document: IndexDocument) -> None: raise NotImplementedError

    @abstractmethod
    def remove_document(self, unique_id: str) -> None: raise NotImplementedError
