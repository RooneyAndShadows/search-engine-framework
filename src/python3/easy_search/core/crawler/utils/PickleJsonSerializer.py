import importlib
import inspect
from typing import Type

import jsonpickle
from jsonpickle import handlers

from ..serialize.JobTypeHandler import JobTypeHandler
from easy_search.interfaces.crawler.enum.JobType import JobType
from easy_search.interfaces.crawler.utils.IJsonSerializer import IJsonSerializer


class PickleJsonSerializer(IJsonSerializer):

    def deserialize(self, source: dict, destination_type: Type[object]) -> object:
        signature = inspect.signature(destination_type.__init__)
        required_args = signature.parameters.items()
        construct_params = {}
        for (key, value) in required_args:
            if key == 'self':
                continue
            if key not in source:
                raise ValueError('Source does not have parameter "%s"' % key)
            construct_params[key] = source[key]
        constructor = getattr(importlib.import_module(destination_type.__module__), destination_type.__name__)
        obj = constructor(**construct_params)
        for attr in [i for i in destination_type.__dict__ if not callable(i)]:
            if attr in source:
                setattr(obj, attr, source[attr])
        return obj

    def serialize(self, source: object) -> str:
        handlers.register(JobType, JobTypeHandler)
        response = jsonpickle.encode(source, False, False)
        handlers.unregister(JobType)
        return response
