from abc import abstractmethod, ABCMeta

from ...index.IndexDocument import IndexDocument


class IDocumentCommunicator:
    __metaclass__ = ABCMeta

    @abstractmethod
    def add_document(self, document: IndexDocument) -> None: raise NotImplementedError

    @abstractmethod
    def remove_document(self, unique_id: str) -> None: raise NotImplementedError
