from elasticsearch import Elasticsearch, TransportError
from pip._vendor import certifi

from easy_search.core.base.dependency.service import json_serializer
from easy_search.interfaces.base.exception.BasicException import BasicException
from easy_search.interfaces.base.communication.response.BaseResponse import BaseResponse
from easy_search.interfaces.base.communication.response.Error import Error
from easy_search.interfaces.server.index.communication.common.IndexDocument import IndexDocument
from easy_search.interfaces.server.index.communication.request.SearchQuery import SearchQuery
from easy_search.interfaces.server.index.communication.response.SearchResult import SearchResult
from easy_search.interfaces.server.index.manager.IDocumentManager import IDocumentManager


class ElasticDocumentManager(IDocumentManager):
    def __init__(self, server_address: str, index_name: str) -> None:
        self.__client = Elasticsearch([server_address], ca_certs=certifi.where())
        self.__index = index_name
        self.__serializer = json_serializer()

    def add(self, document: IndexDocument) -> BaseResponse:
        response = BaseResponse()
        try:
            elastic_response = self.__client.index(self.__index, 'index', self.__serializer.serialize(document),
                                                   document.unique_id)
            if 'result' not in elastic_response or elastic_response['result'] not in ['created', 'updated']:
                return response.set_error(Error("IntegrationError", 500, "Index failed to add index!"))
            response = BaseResponse(True)
        except BasicException as e:
            response.set_error(Error("InternalServerError", 500, e.message))
        except Exception as e:
            print(e)
            response.set_error(Error("InternalServerError", 500, 'Unknown error occurred!'))
        return response

    def delete(self, unique_id: str) -> BaseResponse:
        response = BaseResponse()
        try:
            elastic_response = self.__client.delete(self.__index, 'index', unique_id)
            if 'result' not in elastic_response or elastic_response['result'] not in ['deleted']:
                return response.set_error(Error("IntegrationError", 500, "Index failed to delete index!"))
            response = BaseResponse(True)
        except TransportError as e:
            if e.status_code == 404:
                response.set_error(Error("ObjectNotFound", e.status_code, 'Document does not exist!'))
            else:
                response.set_error(Error("IntegrationError", e.status_code, 'Unknown integration error!'))
        except BasicException as e:
            response.set_error(Error("InternalServerError", 500, e.message))
        except Exception as e:
            print(e)
            response.set_error(Error("InternalServerError", 500, 'Unknown error occurred!'))
        return response

    def search(self, query: SearchQuery) -> SearchResult:
        elastic_query = []
        elastic_range_query = []
        for criteria in query.searchCriteria:
            elastic_query.append({
                "match": {
                    criteria.field: {
                        "query": criteria.term,
                        "boost": criteria.weight
                    }
                }
            })
        for range_criteria in query.rangeCriteria:
            elastic_range_query.append({
                "range": {
                    range_criteria.field: {
                        "gte": range_criteria.minimum,
                        "lte": range_criteria.maximum,
                        "relation": "within"
                    }
                }
            })
        data = {
            "query": {
                "bool": {
                    "should": elastic_query,
                    "must": elastic_range_query
                }
            },
            "from":  query.page * query.items,
            "size": query.items
        }
        result = SearchResult(False)
        try:
            response = self.__client.search(self.__index, 'index', data)
            if 'hits' not in response:
                result.set_error(Error("InternalServerError", 500, 'Index did not return proper response!'))
            else:
                result = SearchResult(True)
                for hit in response['hits']['hits']:
                    result.add_result(self.__serializer.deserialize(hit['_source'], self.index_object_type))
        except Exception as e:
            result.set_error(Error("InternalServerError", 500, 'Unknown error occurred!'))
        return result
