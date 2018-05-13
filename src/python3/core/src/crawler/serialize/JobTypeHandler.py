from jsonpickle import handlers

from interfaces.src.crawler.enum.JobType import JobType


class JobTypeHandler(handlers.BaseHandler):
    def flatten(self, obj, data):
        return obj.value

    def restore(self, obj):
        return JobType(obj)
