from SolrClient import SolrClient

from ...base.BaseManager import BaseManager
from easy_search.interfaces.base.exception.BasicException import BasicException
from easy_search.interfaces.crawler.communication.response.BaseResponse import BaseResponse
from easy_search.interfaces.crawler.communication.response.Error import Error
from easy_search.interfaces.crawler.index.IndexDocument import IndexDocument
from easy_search.interfaces.crawler.server.data.ISearchEngineContext import ISearchEngineContext
from easy_search.interfaces.crawler.server.manager.IDocumentManager import IDocumentManager


class SOLRDocumentManager(BaseManager, IDocumentManager):
    def __init__(self, context: ISearchEngineContext, server_address: str, index_name: str) -> None:
        super().__init__(context)
        self.client = SolrClient(server_address)
        self.index = index_name

    def add(self, document: IndexDocument) -> BaseResponse:
        response = BaseResponse()
        try:
            document.id = document.unique_id
            doc_body = self.serializer.serialize([document])
            solr_response = self.client.index_json(self.index, doc_body)
            if not solr_response:
                return response.set_error(Error("IntegrationError", 500, "Index failed to add document!"))
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
                return response.set_error(Error("IntegrationError", 500, "Index failed to delete document!"))
            self.client.commit(self.index, openSearcher=True, waitSearcher=False)
            response = BaseResponse(True)
        except BasicException as e:
            response.set_error(Error("InternalServerError", 500, e.message))
        except Exception as e:
            print(e)
            response.set_error(Error("InternalServerError", 500, 'Unknown error occurred!'))
        return response
