from easy_search.core.crawler.dependency.service import json_serializer
from easy_search.interfaces.crawler.communication.response.BaseResponse import BaseResponse
from easy_search.interfaces.crawler.index.IndexDocument import IndexDocument


class Document(IndexDocument):
    title = ""
    description = ""

    def __init__(self, unique_id: str) -> None:
        super().__init__(unique_id)


serializer = json_serializer()
print(vars(serializer.deserialize({"unique_id": 'test_id'}, Document)))
print(serializer.serialize(BaseResponse))
