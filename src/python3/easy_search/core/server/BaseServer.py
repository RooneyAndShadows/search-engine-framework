from abc import ABCMeta
from typing import Type

from easy_search.core.base.dependency.service import json_serializer
from easy_search.core.server.dependency.server import job_scheduler
from easy_search.interfaces.server.job.data.ISearchEngineContext import ISearchEngineContext
from easy_search.interfaces.server.index.manager.IDocumentManager import IDocumentManager


class BaseServer:
    __metaclass__ = ABCMeta

    def __init__(self, index_type: Type[object], context: ISearchEngineContext,
                 document_manager: IDocumentManager) -> None:
        self.job_scheduler = job_scheduler(context)
        self.serializer = json_serializer()
        self.documents = document_manager
        self.index_type = index_type
        self.documents.index_object_type = index_type
