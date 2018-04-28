from typing import Optional
from uuid import UUID
from wsgiref.simple_server import make_server

from pyramid.config import Configurator
from pyramid.request import Request
from pyramid.response import Response
from pyramid.view import view_config

from core.src.crawler.server.BaseServer import BaseServer
from interfaces.src.crawler.communication.request.JobResult import JobResult
from interfaces.src.crawler.server.data.ISearchEngineContext import ISearchEngineContext
from interfaces.src.crawler.server.rest.IRestServer import IRestServer


class PyramidServer(IRestServer, BaseServer):
    def __init__(self, context: ISearchEngineContext) -> None:
        super().__init__(context)
        with Configurator() as config:
            config.add_route('register_job', self.JOB_REGISTER_PATH)
            config.add_route('next_job', self.JOB_FETCH_PATH)
            config.add_view(self.register_job, route_name='register_job')
            config.add_view(self.get_next_free, route_name='next_job')
            self._application = config.make_wsgi_app()
        self._server = None

    def authenticate(self, request: Request) -> Optional[UUID]:
        token = request.headers.get("AUTH_TOKEN", None)
        if token is None:
            return token
        try:
            return UUID(token, version=4)
        except Exception:
            return None

    @view_config(
        request_method='POST'
    )
    def register_job(self, request: Request):
        crawler_id = self.authenticate(request)
        if crawler_id is None:
            return Response("", self.FORBIDDEN)
        job_request = request.json_body
        if "job_id" not in job_request:
            return Response("Job id is not provided!", 400)
        job_id_string = job_request["job_id"]
        try:
            job_id = UUID(job_id_string, version=4)
        except Exception:
            return Response("Job id is not valid!", 400)
        job_result = JobResult(job_id, [])
        response = self.job_scheduler.finish_job(crawler_id, job_result)
        if response.is_successful:
            return Response(response.serialize())
        else:
            return Response(response.serialize(), 500)

    @view_config(
        request_method='GET'
    )
    def get_next_free(self, request: Request):
        crawler_id = self.authenticate(request)
        if crawler_id is None:
            return Response("", self.FORBIDDEN)
        response = self.job_scheduler.get_next_job(crawler_id)
        if response.is_successful:
            return Response(response.serialize())
        else:
            return Response(response.serialize(), 500)

    def run(self, host: str = '127.0.0.1', port: int = 8888, debug: bool = False) -> None:
        self._server = make_server(host, port, self._application)
        self._server.serve_forever()
