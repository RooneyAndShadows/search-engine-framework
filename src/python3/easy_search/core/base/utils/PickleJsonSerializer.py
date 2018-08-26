import importlib
import inspect
from enum import EnumMeta, Enum
from typing import Type
from uuid import UUID

import jsonpickle
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
            elif isinstance(source[key], list):
                source[key] = self.deserialize_list(source[key], list(annotation.__args__).pop())
            construct_params[key] = source[key]
        constructor = getattr(importlib.import_module(destination_type.__module__), destination_type.__name__)
        obj = constructor(**construct_params)
        for attr in [i for i in destination_type.__dict__ if not callable(i)]:
            if attr in source:
                setattr(obj, attr, source[attr])
        return obj

    def serialize_list(self, source:list) -> list:
        list_array = []
        for element in source:
            if isinstance(element, object) and hasattr(element, '__dict__'):
                list_array.append(self.serialize_prepare(element))
            else:
                list_array.append(element)
        return list_array

    def serialize_prepare(self, source: object) -> dict:
        required_args = source.__dict__
        ddict = {}
        for key, value in required_args.items():
            if key[0] == '_' or callable(value):
                continue
            if isinstance(value, UUID):
                value = value.hex
            elif isinstance(value, Enum):
                value = value.value
            elif isinstance(value, list):
                value = self.serialize_list(value)
            elif isinstance(value, object) and hasattr(value, '__dict__'):
                value = self.serialize_prepare(value)
            ddict[key] = value
        return ddict

    def serialize(self, source: object) -> str:
        ddict = self.serialize_prepare(source)
        response = jsonpickle.encode(ddict, False, False)
        return response
