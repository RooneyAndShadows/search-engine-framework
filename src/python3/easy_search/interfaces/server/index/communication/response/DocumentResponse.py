from easy_search.interfaces.base.communication.response.BaseResponse import BaseResponse
from easy_search.interfaces.server.index.communication.common.IndexDocument import IndexDocument


class DocumentResponse(BaseResponse):
    def __init__(self, is_successful: bool = False, document: IndexDocument = None):
        super().__init__(is_successful)
        self.document = document
