import importlib
import inspect
from enum import EnumMeta
from typing import Type, GenericMeta
from uuid import UUID

import jsonpickle
from jsonpickle import handlers

from easy_search.core.crawler.serialize.UUIDHandler import UUIDHandler
from easy_search.core.crawler.serialize.JobTypeHandler import JobTypeHandler
from easy_search.interfaces.base.enum.JobType import JobType
from easy_search.interfaces.base.utils.IJsonSerializer import IJsonSerializer


class PickleJsonSerializer(IJsonSerializer):

    def deserialize_list(self, source:list, inner_type: Type[object]) -> list:
        list_array = []
        for element in source:
            if isinstance(element, dict):
                list_array.append(self.deserialize(element, inner_type))
            else:
                list_array.append(element)
        return list_array

    def deserialize(self, source: dict, destination_type: Type[object]) -> object:
        signature = inspect.signature(destination_type.__init__)
        required_args = signature.parameters.items()
        construct_params = {}
        for (key, value) in required_args:
            if key == 'self':
                continue
            if key not in source:
                raise ValueError('Source does not have parameter "%s"' % key)
            annotation = value.annotation
            if annotation is UUID:
                source[key] = UUID(source[key])
            elif isinstance(annotation, EnumMeta):
                source[key] = annotation(source[key])
            elif isinstance(source[key], dict):
                source[key] = self.deserialize(source[key], annotation)
            elif isinstance(source[key], list) and isinstance(annotation, GenericMeta):
                source[key] = self.deserialize_list(source[key], list(annotation.__args__).pop())
            construct_params[key] = source[key]
        constructor = getattr(importlib.import_module(destination_type.__module__), destination_type.__name__)
        obj = constructor(**construct_params)
        for attr in [i for i in destination_type.__dict__ if not callable(i)]:
            if attr in source:
                setattr(obj, attr, source[attr])
        return obj

    def serialize(self, source: object) -> str:
        handlers.register(JobType, JobTypeHandler)
        handlers.register(UUID, UUIDHandler)
        response = jsonpickle.encode(source, False, False)
        handlers.unregister(JobType)
        handlers.unregister(UUID)
        return response
