from easy_search.interfaces.base.enum.JobType import JobType


class JobDescription:
    def __init__(self, job_type: JobType, target: str, plugin_type: str):
        self.job_type = job_type
        self.target = target
        self.plugin_type = plugin_type
