from http.server import HTTPServer
from typing import Optional
from uuid import UUID

from core.src.crawler.server.dependency.server import job_scheduler
from interfaces.src.crawler.server.data.ISearchEngineContext import ISearchEngineContext
from interfaces.src.crawler.server.rest.IRestServer import IRestServer


class HTTPServerWrapper(HTTPServer):

    def __init__(self, server_address, RequestHandlerClass, context: ISearchEngineContext, bind_and_activate=True):
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)
        self.job_scheduler = job_scheduler(context)

    def authenticate(self, headers: dict) -> Optional[UUID]:
        token = headers.get("AUTH_TOKEN", None)
        if token is None:
            return token
        try:
            return UUID(token, version=4)
        except Exception:
            return None

    def register_job(self, headers):
        crawler_id = self.authenticate(headers)
        if crawler_id is None:
            return "", IRestServer.FORBIDDEN
        '''ob_request = request.get_json(True)
        if "job_id" not in job_request:
            return "Job id is not provided!", 400
        job_id_string = job_request["job_id"]
        try:
            job_id = UUID(job_id_string, version=4)
        except Exception:
            return "Job id is not valid!", 400
        job_result = JobResult(job_id, [])
        response = self.job_scheduler.finish_job(crawler_id, job_result)
        if response.is_successful:
            return response.serialize()
        else:
            return response.serialize(), 500'''

    def get_next_free(self, headers):
        crawler_id = self.authenticate(headers)
        if crawler_id is None:
            return "", IRestServer.FORBIDDEN
        response = self.job_scheduler.get_next_job(crawler_id)
        if response.is_successful:
            return response.serialize(), IRestServer.SUCCESS
        else:
            return response.serialize(), IRestServer.INTERNAL_SERVER_ERROR
