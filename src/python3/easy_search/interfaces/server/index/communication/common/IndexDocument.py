from abc import ABC


class IndexDocument(object):
    __metaclass__ = ABC

    def __init__(self, unique_id: str) -> None:
        self.unique_id = unique_id
