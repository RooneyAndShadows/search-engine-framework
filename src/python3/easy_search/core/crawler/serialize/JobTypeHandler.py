from jsonpickle import handlers

from easy_search.interfaces.crawler.enum.JobType import JobType


class JobTypeHandler(handlers.BaseHandler):
    def flatten(self, obj, data):
        return obj.value

    def restore(self, obj):
        return JobType(obj)
