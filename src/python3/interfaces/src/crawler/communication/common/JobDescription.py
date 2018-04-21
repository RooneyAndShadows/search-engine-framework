from interfaces.src.crawler.enum.JobType import JobType


class JobDescription:
    def __init__(self, job_type: JobType = None, target: str = None):
        self.job_type = job_type
        self.target = target
