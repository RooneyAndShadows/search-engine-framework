from typing import Dict

from easy_search.core.crawler.exception.IncorrectJobDescriptionException import IncorrectJobDescriptionException
from easy_search.core.base.dependency.service import hash_generator
from easy_search.interfaces.crawler.process import ICrawler
from easy_search.interfaces.crawler.process import ICrawlerPlugin
from easy_search.interfaces.crawler.utils.IDocumentCommunicator import IDocumentCommunicator
from easy_search.interfaces.crawler.utils.IJobCommunicator import IJobCommunicator


class Crawler(ICrawler):

    def __init__(self, available_plugins: Dict[str, ICrawlerPlugin], job_communicator: IJobCommunicator,
                 document_communicator: IDocumentCommunicator) -> None:
        self.job_communicator = job_communicator
        self.document_communicator = document_communicator
        self.available_plugins = available_plugins
        self.hash_generator = hash_generator()

    def do_next_job(self) -> None:
        plugin_types = list(self.available_plugins.keys())
        next_job = self.job_communicator.get_next_job(plugin_types)
        if next_job.plugin_type not in plugin_types:
            return
        plugin = self.available_plugins[next_job.plugin_type]
        try:
            result, document_list, delete_list = plugin.do_job(next_job)
            self.job_communicator.finish_job(result)
            for document in document_list:
                self.document_communicator.add_document(document)
            for unique_id in delete_list:
                self.document_communicator.remove_document(unique_id)
        except IncorrectJobDescriptionException:
            self.job_communicator.delete_job(next_job.job_id)
            self.document_communicator.remove_document(self.hash_generator.generate_target_hash(next_job.target))
