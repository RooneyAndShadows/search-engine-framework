from typing import Type

from ..BaseHTTPRestServer import BaseHTTPRestServer
from .HTTPHandler import HTTPHandler
from .HTTPServerWrapper import HTTPServerWrapper
from easy_search.interfaces.crawler.server.data.ISearchEngineContext import ISearchEngineContext
from easy_search.interfaces.crawler.server.manager.IDocumentManager import IDocumentManager


class BasicHTTPServer(BaseHTTPRestServer):
    def __init__(self, index_type: Type[object], context: ISearchEngineContext,
                 document_manager: IDocumentManager) -> None:
        super().__init__(index_type, context, document_manager)

    def run(self, host: str = '127.0.0.1', port: int = 8888, debug: bool = False) -> None:
        server = HTTPServerWrapper((host, port), HTTPHandler, self)
        print('Started http Server on host ', host, ':', port)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            server.server_close()


