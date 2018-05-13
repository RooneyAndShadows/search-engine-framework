from elasticsearch import Elasticsearch, TransportError

from core.src.crawler.server.manager.base.BaseManager import BaseManager
from interfaces.src.base.exception.BasicException import BasicException
from interfaces.src.crawler.communication.response.BaseResponse import BaseResponse
from interfaces.src.crawler.communication.response.Error import Error
from interfaces.src.crawler.index.IndexDocument import IndexDocument
from interfaces.src.crawler.server.data.ISearchEngineContext import ISearchEngineContext
from interfaces.src.crawler.server.manager.IDocumentManager import IDocumentManager


class ElasticDocumentManager(BaseManager, IDocumentManager):

    def __init__(self, context: ISearchEngineContext, server_address: str, index_name: str) -> None:
        super().__init__(context)
        self.client = Elasticsearch([server_address])
        self.index = index_name

    def add(self, document: IndexDocument) -> BaseResponse:
        response = BaseResponse()
        try:
            elastic_response = self.client.index(self.index, 'document', self.serializer.serialize(document),
                                                 document.unique_id)
            if 'result' not in elastic_response or elastic_response['result'] not in ['created', 'updated']:
                return response.set_error(Error("IntegrationError", 500, "Index failed to add document!"))
            response = BaseResponse(True)
        except BasicException as e:
            response.set_error(Error("InternalServerError", 500, e.message))
        except Exception:
            response.set_error(Error("InternalServerError", 500, 'Unknown error occurred!'))
        return response

    def delete(self, unique_id: str) -> BaseResponse:
        response = BaseResponse()
        try:
            elastic_response = self.client.delete(self.index, 'document', unique_id)
            if 'result' not in elastic_response or elastic_response['result'] not in ['deleted']:
                return response.set_error(Error("IntegrationError", 500, "Index failed to delete document!"))
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
