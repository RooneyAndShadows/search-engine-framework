import hashlib

from easy_search.interfaces.crawler.utils.IHashGenerator import IHashGenerator


class Sha256HashGenerator(IHashGenerator):

    def generate_target_hash(self, target: str) -> str:
        return hashlib.sha256(target.encode()).hexdigest()
