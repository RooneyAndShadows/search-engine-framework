from ..client.utils.communication.http.JobCommunicator import JobCommunicator
from easy_search.interfaces.crawler.client.utils.IJobCommunicator import IJobCommunicator


def job_communicator() -> IJobCommunicator:
    return JobCommunicator()