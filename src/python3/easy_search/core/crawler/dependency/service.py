from ..utils.PickleJsonSerializer import PickleJsonSerializer
from ..utils.Sha256HashGenerator import Sha256HashGenerator
from easy_search.interfaces.crawler.utils.IHashGenerator import IHashGenerator
from easy_search.interfaces.crawler.utils.IJsonSerializer import IJsonSerializer


def hash_generator() -> IHashGenerator:
    return Sha256HashGenerator()


def json_serializer() -> IJsonSerializer:
    return PickleJsonSerializer()
