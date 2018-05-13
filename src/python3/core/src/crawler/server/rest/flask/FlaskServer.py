from typing import Optional, TypeVar, Type
from uuid import UUID

from flask import Flask, request

from core.src.crawler.server.rest.BaseHTTPRestServer import BaseHTTPRestServer
from interfaces.src.crawler.server.data.ISearchEngineContext import ISearchEngineContext
from interfaces.src.crawler.server.manager.IDocumentManager import IDocumentManager


class FlaskServer(BaseHTTPRestServer):

    def __init__(self, name: str, index_type: Type[object], context: ISearchEngineContext,
                 manager: IDocumentManager) -> None:
        super().__init__(index_type, context, manager)
        self._application = Flask(name)
        self._config()

    def _config(self):
        self._application.add_url_rule(self.JOB_REGISTER_PATH, 'register_job',
                                       lambda: self.register_job(request.headers, request.get_json(True)),
                                       methods=["POST"])
        self._application.add_url_rule(self.JOB_FETCH_PATH, 'fetch_job',
                                       lambda: self.get_next_free(request.headers),
                                       methods=["GET"])
        self._application.add_url_rule(self.DOCUMENT_ADD, 'add_document',
                                       lambda: self.add_document(request.headers, request.get_json(True)),
                                       methods=["POST"])
        self._application.add_url_rule(self.DOCUMENT_DELETE + '/<doc_id>', 'delete_document',
                                       lambda doc_id: self.delete_document(request.headers, doc_id),
                                       methods=["DELETE"])

    def run(self, host: str = '127.0.0.1', port: int = 8888, debug: bool = False) -> None:
        self._application.run(host, port, debug)
