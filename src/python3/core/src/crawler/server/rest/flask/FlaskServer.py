from typing import Optional
from uuid import UUID

from flask import Flask, request, jsonify

from core.src.crawler.server.BaseServer import BaseServer
from interfaces.src.crawler.communication.request.JobResult import JobResult
from interfaces.src.crawler.server.data.ISearchEngineContext import ISearchEngineContext
from interfaces.src.crawler.server.rest.IRestServer import IRestServer


class FlaskServer(BaseServer, IRestServer):

    def __init__(self, name: str, context: ISearchEngineContext) -> None:
        super().__init__(context)
        self._application = Flask(name)
        self._config()

    def _config(self):
        self._application.add_url_rule(self.JOB_REGISTER_PATH, 'register_job', self.register_job, methods=["POST"])
        self._application.add_url_rule(self.JOB_FETCH_PATH, 'fetch_job', self.get_next_free, methods=["GET"])

    def run(self, host: str = '127.0.0.1', port: int = 8888, debug: bool = False) -> None:
        self._application.run(host, port, debug)

    def authenticate(self) -> Optional[UUID]:
        token = request.headers.get("AUTH_TOKEN", None)
        if token is None:
            return token
        try:
            return UUID(token, version=4)
        except Exception:
            return None

    def register_job(self):
        crawler_id = self.authenticate()
        if crawler_id is None:
            return "", self.FORBIDDEN
        job_request = request.get_json(True)
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
            return response.serialize(), 500

    def get_next_free(self):
        crawler_id = self.authenticate()
        if crawler_id is None:
            return "", self.FORBIDDEN
        response = self.job_scheduler.get_next_job(crawler_id)
        if response.is_successful:
            return response.serialize()
        else:
            return response.serialize(), 500
