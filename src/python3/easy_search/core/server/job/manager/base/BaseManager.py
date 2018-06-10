from abc import ABCMeta

from easy_search.core.base.dependency.service import json_serializer
from easy_search.core.server.job.repository.Repository import Repository
from easy_search.interfaces.server.job.data.ISearchEngineContext import ISearchEngineContext


class BaseManager:

    def __init__(self, context: ISearchEngineContext) -> None:
        self.context = context
        self.repository = Repository(context)
        self.serializer = json_serializer()
