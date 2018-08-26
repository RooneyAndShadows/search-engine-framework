from uuid import uuid4

from easy_search.core.base.dependency.service import json_serializer
from easy_search.interfaces.base.communication.response.BaseResponse import BaseResponse
from easy_search.interfaces.base.enum.JobType import JobType
from easy_search.interfaces.base.job.JobDescription import JobDescription
from easy_search.interfaces.server.index.communication.common.IndexDocument import IndexDocument
from easy_search.interfaces.server.job.communication.request.JobResult import JobResult


class Document(IndexDocument):
    title = ""
    description = ""

    def __init__(self, unique_id: str) -> None:
        super().__init__(unique_id)


serializer = json_serializer()
print(vars(serializer.deserialize({"job_id": '179dc51ec14949fe9d7427771ca267fb', "job_list": [
    {"job_type": 1, "target": "123", "plugin_type": 123}
]}, JobResult)))
print(serializer.serialize(JobResult(uuid4(), [JobDescription(JobType.EXTRACT, '123', '123')])))
