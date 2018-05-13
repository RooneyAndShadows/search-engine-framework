from ....dependency.service import json_serializer
from ...repository.Repository import Repository
from easy_search.interfaces.crawler.server.data.ISearchEngineContext import ISearchEngineContext


class BaseManager:
    def __init__(self, context: ISearchEngineContext) -> None:
        self.context = context
        self.repository = Repository(context)
        self.serializer = json_serializer()
