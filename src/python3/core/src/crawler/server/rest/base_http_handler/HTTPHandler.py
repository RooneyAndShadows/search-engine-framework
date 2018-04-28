from http.server import BaseHTTPRequestHandler

from core.src.crawler.server.rest.base_http_handler.HTTPServerWrapper import HTTPServerWrapper
from interfaces.src.crawler.server.rest.IRestServer import IRestServer


class HTTPHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server: HTTPServerWrapper):
        super().__init__(request, client_address, server)

    def do_GET(self):
        if self.path != '/job/next':
            self.send_response(IRestServer.NOT_FOUND)
            return
        response, code = self.server.get_next_free(self.headers)
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(response, 'utf-8'))

    def do_POST(self):
        if self.path != '/job/register':
            self.send_response(IRestServer.NOT_FOUND)
            return
        response, code = self.server.register_job(self.headers)
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(response, 'utf-8'))
