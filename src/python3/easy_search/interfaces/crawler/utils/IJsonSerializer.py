from abc import ABCMeta, abstractmethod
from typing import Type


class IJsonSerializer:
    __metaclass__ = ABCMeta

    @abstractmethod
    def serialize(self, source: object) -> str: raise NotImplementedError

    @abstractmethod
    def deserialize(self, source: dict, destination_type: Type[object]): raise NotImplementedError
