from easy_search.core.crawler.utils.communication.http import JobCommunicator
from easy_search.interfaces.crawler.utils.IJobCommunicator import IJobCommunicator


def job_communicator() -> IJobCommunicator:
    return JobCommunicator()