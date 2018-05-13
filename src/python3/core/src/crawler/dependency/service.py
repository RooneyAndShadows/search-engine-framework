from core.src.crawler.utils.PickleJsonSerializer import PickleJsonSerializer
from core.src.crawler.utils.Sha256HashGenerator import Sha256HashGenerator
from interfaces.src.crawler.utils.IHashGenerator import IHashGenerator
from interfaces.src.crawler.utils.IJsonSerializer import IJsonSerializer


def hash_generator() -> IHashGenerator:
    return Sha256HashGenerator()


def json_serializer() -> IJsonSerializer:
    return PickleJsonSerializer()
