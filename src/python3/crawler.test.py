from typing import Tuple, List
from uuid import UUID
from lxml.html import document_fromstring

from requests import Response

from easy_search.core.crawler.process.Crawler import Crawler
from easy_search.core.crawler.process.plugin.BaseHTTPCrawlerPlugin import BaseHTTPCrawlerPlugin
from easy_search.core.crawler.utils.communication.http import DocumentCommunicator
from easy_search.core.crawler.utils.communication.http import JobCommunicator
from easy_search.core.base.dependency.service import hash_generator
from easy_search.interfaces.base.job.JobDescription import JobDescription
from easy_search.interfaces.base.enum import JobType
from easy_search.interfaces.server.index.communication.common.IndexDocument import IndexDocument


class Property(IndexDocument):
    def __init__(self, unique_id: str, title: str) -> None:
        super().__init__(unique_id)
        self.title = title


class BPBPlugin(BaseHTTPCrawlerPlugin):

    def parse_response(self, response: Response, job_type: JobType) -> Tuple[List[IndexDocument], List[JobDescription]]:
        if job_type == JobType.EXTRACT:
            text = response.text
            document = document_fromstring(text)
            hasher = hash_generator()
            for e in document.cssselect("div.rh_page__property_title"):
                title = e.text_content()
                return [Property(hasher.generate_target_hash(response.url), title)], []


plugins = {"bpb": BPBPlugin()}
crawler = Crawler(plugins, JobCommunicator("http://127.0.0.1:8888",  UUID("5a84baf2-8ea8-4481-8809-027589255f81")),
                  DocumentCommunicator("http://127.0.0.1:8888", UUID("5a84baf2-8ea8-4481-8809-027589255f81")))
crawler.do_next_job()
