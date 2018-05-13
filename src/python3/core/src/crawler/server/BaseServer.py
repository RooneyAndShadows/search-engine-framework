from abc import ABCMeta
from typing import Type

from core.src.crawler.dependency.server import job_scheduler
from core.src.crawler.dependency.service import json_serializer
from interfaces.src.crawler.server.data.ISearchEngineContext import ISearchEngineContext
from interfaces.src.crawler.server.manager.IDocumentManager import IDocumentManager


class BaseServer:
    __metaclass__ = ABCMeta

    def __init__(self, index_type: Type[object], context: ISearchEngineContext,
                 document_manager: IDocumentManager) -> None:
        self.job_scheduler = job_scheduler(context)
        self.serializer = json_serializer()
        self.documents = document_manager
        self.index_type = index_type
