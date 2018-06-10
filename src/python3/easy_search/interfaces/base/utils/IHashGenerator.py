from abc import ABCMeta, abstractmethod


class IHashGenerator:
    __metaclass__ = ABCMeta

    @abstractmethod
    def generate_target_hash(self, target: str) -> str: raise NotImplementedError
