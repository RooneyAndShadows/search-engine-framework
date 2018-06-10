import urllib.parse

import requests

from .....server.rest.BaseHTTPRestServer import BaseHTTPRestServer
from easy_search.interfaces.crawler.utils.IDocumentCommunicator import IDocumentCommunicator
from easy_search.interfaces.server.index.communication.common.IndexDocument import IndexDocument
from .BaseCommunicator import BaseCommunicator


class DocumentCommunicator(IDocumentCommunicator, BaseCommunicator):
    def add_document(self, document: IndexDocument) -> None:
        url = urllib.parse.urljoin(self.base_url, BaseHTTPRestServer.DOCUMENT_ADD)
        data = self.serialize.serialize(document)
        response = requests.post(url, data, headers=self.http_headers)
        self.validate_response(response)

    def remove_document(self, unique_id: str) -> None:
        url = urllib.parse.urljoin(self.base_url, BaseHTTPRestServer.DOCUMENT_DELETE + "/" + unique_id)
        response = requests.delete(url, headers=self.http_headers)
        self.validate_response(response)
