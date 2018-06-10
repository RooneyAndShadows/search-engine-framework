import json
import re
from typing import Type
from wsgiref.simple_server import make_server
from wsgiref.util import request_uri
from urllib.parse import urlparse

from ..BaseHTTPRestServer import BaseHTTPRestServer
from easy_search.interfaces.server.job.data.ISearchEngineContext import ISearchEngineContext
from easy_search.interfaces.server.index.manager import IDocumentManager


class BasicHTTPServer(BaseHTTPRestServer):
    STATUS_MAPPING = {
        BaseHTTPRestServer.NOT_FOUND: str(BaseHTTPRestServer.NOT_FOUND) + ' NOT FOUND',
        BaseHTTPRestServer.BAD_REQUEST: str(BaseHTTPRestServer.BAD_REQUEST) + ' BAD REQUEST',
        BaseHTTPRestServer.FORBIDDEN: str(BaseHTTPRestServer.FORBIDDEN) + ' FORBIDDEN',
        BaseHTTPRestServer.INTERNAL_SERVER_ERROR:
            str(BaseHTTPRestServer.INTERNAL_SERVER_ERROR) + ' INTERNAL SERVER ERROR',
        BaseHTTPRestServer.SUCCESS: str(BaseHTTPRestServer.SUCCESS) + ' SUCCESS',
    }

    def __init__(self, index_type: Type[object], context: ISearchEngineContext,
                 document_manager: IDocumentManager) -> None:
        super().__init__(index_type, context, document_manager)

    def manage_response_wsgi(self, response: str, code: int, start_response):
        start_response(self.STATUS_MAPPING.get(code, '500 INTERNAL SERVER ERROR'), [
            ('Content-Type', 'application/json'),
            ('Content-Length', str(len(response)))
        ])
        return [bytes(response, 'utf-8')]

    def do_GET(self, path: str, headers: dict, start_response):
        if path != '/job/next':
            response, code = "", self.NOT_FOUND
        else:
            response, code = self.get_next_free(headers)
        return self.manage_response_wsgi(response, code, start_response)

    def do_POST(self, path: str, raw_request: str, headers: dict, start_response):
        request = json.loads(raw_request)
        if path == self.JOB_REGISTER_PATH:
            response, code = self.register_job(headers, request)
        elif path == self.DOCUMENT_ADD:
            response, code = self.add_document(headers, request)
        elif path == self.DOCUMENT_SEARCH:
            response, code = self.search(headers, request)
        else:
            response, code = "", self.NOT_FOUND
        return self.manage_response_wsgi(response, code, start_response)

    def do_DELETE(self, path: str, headers: dict, start_response):
        output = re.search(self.DOCUMENT_DELETE + '/(.*)', path)
        if output is None:
            response, code = "", self.NOT_FOUND
        else:
            response, code = self.delete_document(headers, output.group(1))
        return self.manage_response_wsgi(response, code, start_response)

    def application(self, environ, start_response):
        path = request_uri(environ)
        try:
            path_info = urlparse(path)
            if not (path_info.scheme and path_info.netloc and path_info.path):
                return self.manage_response_wsgi("", self.INTERNAL_SERVER_ERROR, start_response)
        except Exception:
            return self.manage_response_wsgi("", self.INTERNAL_SERVER_ERROR, start_response)
        headers = dict((k.replace("HTTP_", ""), v) for (k, v) in environ.items() if re.match('^HTTP_.*', k))
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        except ValueError:
            request_body_size = 0
        raw_request = environ["wsgi.input"].read(request_body_size)
        if environ['REQUEST_METHOD'] == 'GET':
            return self.do_GET(path_info.path, headers, start_response)
        elif environ['REQUEST_METHOD'] == 'POST':
            return self.do_POST(path_info.path, raw_request, headers, start_response)
        elif environ['REQUEST_METHOD'] == 'DELETE':
            return self.do_DELETE(path_info.path, headers, start_response)
        else:
            return self.manage_response_wsgi("", self.NOT_FOUND, start_response)

    def run_dev(self, host: str = '127.0.0.1', port: int = 8888, debug: bool = False) -> None:
        server = make_server(host, port, self.application)
        print('Started http Server on host ', host, ':', port)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            server.server_close()

    def get_wsgi_application(self):
        return self.application
