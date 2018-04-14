import datetime
import hashlib
import uuid
from uuid import UUID

from sqlalchemy import asc

from core.src.crawler.server.data.sqlalchemy.entity.Job import Job
from core.src.crawler.server.data.sqlalchemy.set.base.BaseSet import BaseSet
from interfaces.src.crawler.enum.JobType import JobType
from interfaces.src.crawler.server.data.data.JobData import JobData
from interfaces.src.crawler.server.data.entity.Job import Job as JobDTO
from interfaces.src.crawler.server.data.set.IJobSet import IJobSet


class JobSet(BaseSet, IJobSet):
    def convert(self, entity: Job) -> JobDTO:
        job = JobDTO(entity.id, JobType(entity.type), entity.url, entity.hash, entity.locked,
                     entity.date_added, entity.crawler_id)
        if entity.done_by is not None:
            job.set_executor_crawler_id(entity.done_by, entity.date_done)
        return job

    def fill(self, data: JobData, job: Job) -> None:
        job.date_done = data.date_executed
        job.done_by = data.executor_id
        job.crawler_id = data.creator_id
        job.locked = data.locked
        job.hash = hashlib.sha256(data.target.encode()).hexdigest()
        job.url = data.target
        job.type = data.type.value

    def add(self, job: JobData) -> UUID:
        entity = Job()
        self.fill(job, entity)
        entity.date_added = datetime.datetime.now()
        entity.id = uuid.uuid4()
        self.session.add(entity)
        return entity.id

    def edit(self, job_id: UUID, job: JobData) -> None:
        query = self.session.query(Job)
        entity = query \
            .filter(Job.id == job_id) \
            .one()
        self.fill(job, entity)

    def delete(self, job_id: UUID) -> None:
        query = self.session.query(Job)
        entity = query \
            .filter(Job.id == job_id) \
            .one()
        return self.session.delete(entity)

    def get(self, job_id: UUID) -> Job:
        query = self.session.query(Job)
        entity = query \
            .filter(Job.id == job_id) \
            .one()
        return self.convert(entity)

    def get_by_hash(self, unique_hash: str) -> Job:
        query = self.session.query(Job)
        entity = query \
            .filter(Job.hash == unique_hash) \
            .one()
        return self.convert(entity)

    def get_next_free(self) -> Job:
        query = self.session.query(Job)
        entity = query\
            .order_by(asc(Job.date_added))\
            .filter(Job.locked == False)\
            .first()
        return self.convert(entity)

    def lock(self, job_id: UUID) -> None:
        query = self.session.query(Job)
        entity = query \
            .filter(Job.id == job_id) \
            .one()
        entity.locked = True

    def unlock(self, job_id: UUID) -> None:
        query = self.session.query(Job)
        entity = query \
            .filter(Job.id == job_id) \
            .one()
        entity.locked = False
