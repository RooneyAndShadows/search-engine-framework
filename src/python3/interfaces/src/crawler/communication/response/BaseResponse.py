import jsonpickle
from jsonpickle import handlers

from interfaces.src.base.serialize.JobTypeHandler import JobTypeHandler
from interfaces.src.crawler.communication.response.Error import Error
from interfaces.src.crawler.enum.JobType import JobType


class BaseResponse(object):
    def __init__(self, is_successful: bool = False):
        self.is_successful = is_successful
        self.error = None

    def set_error(self, error: Error) -> None:
        self.error = error

    def has_error(self) -> bool:
        return self.error is not None

    def serialize(self):
        handlers.register(JobType, JobTypeHandler)
        response = jsonpickle.encode(self, False)
        handlers.unregister(JobType)
        return response
