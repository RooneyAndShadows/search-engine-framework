from easy_search.core.base.utils.PickleJsonSerializer import PickleJsonSerializer
from easy_search.core.base.utils import Sha256HashGenerator
from easy_search.interfaces.base.utils.IHashGenerator import IHashGenerator
from easy_search.interfaces.base.utils.IJsonSerializer import IJsonSerializer


def hash_generator() -> IHashGenerator:
    return Sha256HashGenerator()


def json_serializer() -> IJsonSerializer:
    return PickleJsonSerializer()
