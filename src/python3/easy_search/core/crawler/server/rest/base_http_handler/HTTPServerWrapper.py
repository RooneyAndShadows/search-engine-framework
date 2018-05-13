from http.server import HTTPServer
from ..BaseHTTPRestServer import BaseHTTPRestServer


class HTTPServerWrapper(HTTPServer):
    def __init__(self, server_address, RequestHandlerClass, server: BaseHTTPRestServer, bind_and_activate=True):
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)
        self.rest_server = server
