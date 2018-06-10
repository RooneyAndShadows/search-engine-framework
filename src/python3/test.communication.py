import uuid
from uuid import UUID

from easy_search.core.crawler.utils.communication.http import DocumentCommunicator
from easy_search.core.crawler.utils.communication.http import JobCommunicator
from easy_search.interfaces.base.job.JobDescription import JobDescription
from easy_search.interfaces.server.job.communication import JobResult
from easy_search.interfaces.base.enum import JobType
from easy_search.interfaces.server.index.communication.common.IndexDocument import IndexDocument

base_url = 'http://127.0.0.1:8888'
crawler_id = UUID('5a84baf2-8ea8-4481-8809-027589255f81')

job_communicator = JobCommunicator(base_url, crawler_id)
job_communicator.finish_job(JobResult(UUID('02eb280b-a3ae-4701-b044-431b0aeb78f4'),
                                      [JobDescription(JobType.HARVEST, uuid.uuid4().hex)]))
response = job_communicator.get_next_job()
print(vars(response))

documents = DocumentCommunicator(base_url, crawler_id)
doc_id = uuid.uuid4().hex
documents.add_document(IndexDocument(doc_id))
documents.remove_document(doc_id)
