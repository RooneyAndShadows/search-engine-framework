from easy_search.core.base.dependency.service import json_serializer
from easy_search.interfaces.base.communication.response.BaseResponse import BaseResponse
from easy_search.interfaces.base.communication.response.Error import Error
from easy_search.interfaces.server.index.communication.common import IndexDocument
from easy_search.interfaces.server.index.communication.request.SearchQuery import SearchQuery
from easy_search.interfaces.server.index.communication.response.DocumentResponse import DocumentResponse
from easy_search.interfaces.server.index.communication.response.SearchResult import SearchResult
from easy_search.interfaces.server.index.manager.IDocumentManager import IDocumentManager
from pymongo import MongoClient
from pymongo.collection import Collection


class MongoDBDocumentManager(IDocumentManager):
    def add(self, document: IndexDocument) -> BaseResponse:
        response = BaseResponse()
        try:
            entity = self.get_collection().find_one({"unique_id": document.unique_id.__str__()})
            if entity is None:
                self.get_collection().insert_one(document.__dict__)
            else:
                self.get_collection().find_one_and_replace({"unique_id": document.unique_id.__str__()},
                                                           document.__dict__)

            response = BaseResponse(True)
        except Exception as e:
            response.set_error(Error('InternalServerError', 500, 'Failed to add document to index'))
        return response

    def delete(self, unique_id: str) -> BaseResponse:
        response = BaseResponse()
        try:
            self.get_collection().find_one_and_delete({"unique_id": unique_id.__str__()})
        except Exception as e:
            response.set_error(Error('InternalServerError', 500, 'Failed to delete document to index'))
        return response

    def get(self, unique_id: str) -> DocumentResponse:
        response = DocumentResponse()
        entity = self.get_collection().find_one({"unique_id": unique_id.__str__()})
        if entity is None:
            response.set_error(Error('NotFound', 404, 'Index document not found with given id'))
        else:
            response = DocumentResponse(True, entity)
        return response

    def search(self, query: SearchQuery) -> SearchResult:
        pass

    def __init__(self, database_connection: str, db_name: str) -> None:
        super().__init__()
        self.client = MongoClient(database_connection)
        self.database = self.client[db_name]
        self.serializer = json_serializer()

    def get_collection(self) -> Collection:
        return self.database.documents
