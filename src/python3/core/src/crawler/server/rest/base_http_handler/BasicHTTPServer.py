from http.server import HTTPServer

from core.src.crawler.server.rest.base_http_handler.HTTPHandler import HTTPHandler
from core.src.crawler.server.rest.base_http_handler.HTTPServerWrapper import HTTPServerWrapper
from interfaces.src.crawler.server.data.ISearchEngineContext import ISearchEngineContext
from interfaces.src.crawler.server.rest.IRestServer import IRestServer


class BasicHTTPServer(IRestServer):
    def __init__(self, context: ISearchEngineContext) -> None:
        self.context = context

    def run(self, host: str = '127.0.0.1', port: int = 8888, debug: bool = False) -> None:
        server = HTTPServerWrapper((host, port), HTTPHandler, self.context)
        print('Started HTTP Server on host ', host, ':', port)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        server.server_close()


