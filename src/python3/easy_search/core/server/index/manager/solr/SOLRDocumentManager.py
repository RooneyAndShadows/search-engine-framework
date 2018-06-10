from typing import Type

from SolrClient import SolrClient

from easy_search.core.base.dependency.service import json_serializer
from easy_search.interfaces.base.exception.BasicException import BasicException
from easy_search.interfaces.base.communication.response.BaseResponse import BaseResponse
from easy_search.interfaces.base.communication.response.Error import Error
from easy_search.interfaces.server.index.communication.common.IndexDocument import IndexDocument
from easy_search.interfaces.server.index.communication.request.SearchQuery import SearchQuery
from easy_search.interfaces.server.index.communication.response.SearchResult import SearchResult
from easy_search.interfaces.server.index.manager.IDocumentManager import IDocumentManager


class SOLRDocumentManager(IDocumentManager):

    def __init__(self, server_address: str, index_name: str) -> None:
        self.client = SolrClient(server_address)
        self.index = index_name
        self._serializer = json_serializer()

    def add(self, document: IndexDocument) -> BaseResponse:
        response = BaseResponse()
        try:
            document.id = document.unique_id
            doc_body = self._serializer.serialize([document])
            solr_response = self.client.index_json(self.index, doc_body)
            if not solr_response:
                return response.set_error(Error("IntegrationError", 500, "Index failed to add index!"))
            self.client.commit(self.index, openSearcher=True, waitSearcher=False)
            response = BaseResponse(True)
        except BasicException as e:
            response.set_error(Error("InternalServerError", 500, e.message))
        except Exception as e:
            response.set_error(Error("InternalServerError", 500, 'Unknown error occurred!'))
        return response

    def delete(self, unique_id: str) -> BaseResponse:
        response = BaseResponse()
        try:
            solr_response = self.client.delete_doc_by_id(self.index, unique_id)
            if not solr_response:
                return response.set_error(Error("IntegrationError", 500, "Index failed to delete index!"))
            self.client.commit(self.index, openSearcher=True, waitSearcher=False)
            response = BaseResponse(True)
        except BasicException as e:
            response.set_error(Error("InternalServerError", 500, e.message))
        except Exception as e:
            print(e)
            response.set_error(Error("InternalServerError", 500, 'Unknown error occurred!'))
        return response

    def search(self, query: SearchQuery) -> SearchResult:
        solr_query = ""
        solr_field_query = ""
        solr_range_query = []
        for criteria in query.searchCriteria:
            solr_field_query += criteria.field + '^' + str(criteria.weight) + " "
            words = criteria.term.split(" ")
            for word in words:
                word = word.lower()
                solr_query += " " + word
        for range_criteria in query.rangeCriteria:
            solr_range_query.append(
                range_criteria.field + ":["+str(range_criteria.minimum)+" TO "+str(range_criteria.maximum)+"]")
        data = {
            "q": solr_query.strip(),
            "offset": query.page * query.items,
            "limit": query.items,
            "filter": solr_range_query,
            "defType": "edismax",
            "qf": solr_field_query
        }
        result = SearchResult(False)
        try:
            response = self.client.query_raw(self.index, data)
            result = SearchResult(True)
            for document in response['response']['docs']:
                result.add_result(self._serializer.deserialize(document, self.index_object_type))
        except Exception as e:
            result.set_error(Error("InternalServerError", 500, 'Unknown error occurred!'))
        return result




