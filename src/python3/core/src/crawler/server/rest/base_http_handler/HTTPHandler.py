import json
import re
from http.server import BaseHTTPRequestHandler

from core.src.crawler.server.rest.BaseHTTPRestServer import BaseHTTPRestServer
from core.src.crawler.server.rest.base_http_handler.HTTPServerWrapper import HTTPServerWrapper


class HTTPHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server: HTTPServerWrapper):
        super().__init__(request, client_address, server)
        self.server = server

    def manage_response(self, response: str, code: int):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(response, 'utf-8'))

    def do_GET(self):
        if self.path != '/job/next':
            self.send_response(self.server.rest_server.NOT_FOUND)
            return
        response, code = self.server.rest_server.get_next_free(self.headers)
        self.manage_response(response, code)

    def do_POST(self):
        raw_request = self.rfile.read(int(self.headers['Content-Length']))
        request = json.loads(raw_request)
        if self.path == self.server.rest_server.JOB_REGISTER_PATH:
            response, code = self.server.rest_server.register_job(self.headers)
        elif self.path == self.server.rest_server.DOCUMENT_ADD:
            response, code = self.server.rest_server.add_document(self.headers, request)
        else:
            self.send_response(self.server.rest_server.NOT_FOUND)
            return
        self.manage_response(response, code)

    def do_DELETE(self):
        output = re.search(self.server.rest_server.DOCUMENT_DELETE + '/(.*)', self.path)
        if output is None:
            self.send_response(BaseHTTPRestServer.NOT_FOUND)
            return
        else:
            response, code = self.server.rest_server.delete_document(self.headers, output.group(1))
        self.manage_response(response, code)
