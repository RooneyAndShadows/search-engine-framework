from typing import Type
from wsgiref.simple_server import make_server

from pyramid.config import Configurator
from pyramid.request import Request
from pyramid.response import Response
from pyramid.view import view_config

from ..BaseHTTPRestServer import BaseHTTPRestServer
from easy_search.interfaces.crawler.server.data.ISearchEngineContext import ISearchEngineContext
from easy_search.interfaces.crawler.server.manager.IDocumentManager import IDocumentManager


class PyramidServer(BaseHTTPRestServer):
    def __init__(self, index_type: Type[object], context: ISearchEngineContext, manager: IDocumentManager) -> None:
        super().__init__(index_type, context, manager)
        with Configurator() as config:
            config.add_route('register_job', self.JOB_REGISTER_PATH)
            config.add_route('next_job', self.JOB_FETCH_PATH)
            config.add_route('add_document', self.DOCUMENT_ADD)
            config.add_route('delete_document', self.DOCUMENT_DELETE + '/{id}')
            config.add_view(self.register_job_wrapper, route_name='register_job')
            config.add_view(self.get_next_free_wrapper, route_name='next_job')
            config.add_view(self.add_document_wrapper, route_name='add_document')
            config.add_view(self.delete_document_wrapper, route_name='delete_document')
            self._application = config.make_wsgi_app()
        self._server = None

    @view_config(
        request_method='POST'
    )
    def register_job_wrapper(self, request: Request):
        response, code = self.register_job(request.headers, request.json_body)
        return Response(response, code)

    @view_config(
        request_method='POST'
    )
    def add_document_wrapper(self, request: Request):
        response, code = self.add_document(request.headers, request.json_body)
        return Response(response, code)

    @view_config(
        request_method='GET'
    )
    def get_next_free_wrapper(self, request: Request):
        response, code = self.get_next_free(request.headers)
        return Response(response, code)

    @view_config(
        request_method='DELETE'
    )
    def delete_document_wrapper(self, request: Request):
        response, code = self.delete_document(request.headers, request.matchdict['id'])
        return Response(response, code)

    def run(self, host: str = '127.0.0.1', port: int = 8888, debug: bool = False) -> None:
        self._server = make_server(host, port, self._application)
        print("Starting server on %s port: %s" % (host, port))
        self._server.serve_forever()
