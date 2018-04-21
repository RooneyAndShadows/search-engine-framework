from core.src.crawler.utils.Sha256HashGenerator import Sha256HashGenerator
from interfaces.src.crawler.utils.IHashGenerator import IHashGenerator


def hash_generator() -> IHashGenerator:
    return Sha256HashGenerator()
