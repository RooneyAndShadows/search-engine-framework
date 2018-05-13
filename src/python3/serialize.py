from core.src.crawler.dependency.service import json_serializer
from interfaces.src.crawler.communication.response.BaseResponse import BaseResponse
from interfaces.src.crawler.index.IndexDocument import IndexDocument


class Document(IndexDocument):
    title = ""
    description = ""

    def __init__(self, unique_id: str) -> None:
        super().__init__(unique_id)


serializer = json_serializer()
print(vars(serializer.deserialize({"unique_id": 'test_id'}, Document)))
print(serializer.serialize(BaseResponse))
