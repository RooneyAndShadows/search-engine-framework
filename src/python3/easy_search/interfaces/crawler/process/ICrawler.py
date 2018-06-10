from abc import ABC, abstractmethod


class ICrawler(object):
    __metaclass__ = ABC

    @abstractmethod
    def do_next_job(self) -> None: raise NotImplementedError
