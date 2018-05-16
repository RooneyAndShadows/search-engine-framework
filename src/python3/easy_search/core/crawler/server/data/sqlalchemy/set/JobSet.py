import datetime
import uuid
from typing import List
from uuid import UUID

from sqlalchemy import asc, and_
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from ..entity.Job import Job
from .base.BaseSet import BaseSet
from .....dependency.service import hash_generator
from easy_search.interfaces.crawler.enum.JobType import JobType
from easy_search.interfaces.crawler.server.data.data.JobData import JobData
from easy_search.interfaces.crawler.server.data.entity.Job import Job as JobDTO
from easy_search.interfaces.crawler.server.data.exception.DataAccessException import DataAccessException
from easy_search.interfaces.crawler.server.data.exception.EntityNotFoundException import EntityNotFoundException
from easy_search.interfaces.crawler.server.data.set.IJobSet import IJobSet


class JobSet(BaseSet, IJobSet):

    def convert(self, entity: Job) -> JobDTO:
        job = JobDTO(entity.id, JobType(entity.type), entity.url, entity.hash, entity.locked,
                     entity.date_added, entity.crawler_id, entity.plugin)
        if entity.done_by is not None:
            job.set_executor_crawler_id(entity.done_by, entity.date_done)
        return job

    def fill(self, data: JobData, job: Job) -> None:
        job.date_done = data.date_executed
        job.done_by = data.executor_id
        job.crawler_id = data.creator_id
        job.locked = data.locked
        job.hash = hash_generator().generate_target_hash(data.target)
        job.url = data.target
        job.plugin = data.plugin_type
        job.type = data.type.value

    def add(self, job: JobData) -> UUID:
        try:
            entity = Job()
            self.fill(job, entity)
            entity.date_added = datetime.datetime.now()
            entity.id = uuid.uuid4()
            self.session.add(entity)
            return entity.id
        except Exception as e:
            raise DataAccessException("Failed to add job to database!", e)

    def edit(self, job_id: UUID, job: JobData) -> None:
        try:
            query = self.session.query(Job)
            entity = query \
                .filter(Job.id == job_id) \
                .one()
            self.fill(job, entity)
        except MultipleResultsFound as e:
            raise EntityNotFoundException("Job id is not unique!", e)
        except NoResultFound as e:
            raise EntityNotFoundException("Job was not found in database!", e)
        except Exception as e:
            raise DataAccessException("Failed to edit job in database!", e)

    def delete(self, job_id: UUID) -> None:
        try:
            query = self.session.query(Job)
            try:
                entity = query \
                    .filter(Job.id == job_id) \
                    .one()
                self.session.delete(entity)
            except MultipleResultsFound:
                entity_list = query.filter(Job.id == job_id).all()
                for entity in entity_list:
                    self.session.delete(entity)
        except NoResultFound:
            pass
        except Exception as e:
            raise DataAccessException("Failed to edit job in database!", e)

    def get(self, job_id: UUID) -> Job:
        try:
            query = self.session.query(Job)
            entity = query \
                .filter(Job.id == job_id) \
                .one()
            return self.convert(entity)
        except MultipleResultsFound as e:
            raise EntityNotFoundException("Job id is not unique!", e)
        except NoResultFound as e:
            raise EntityNotFoundException("Job was not found in database!", e)
        except Exception as e:
            raise DataAccessException("Failed to edit job in database!", e)

    def get_by_hash(self, unique_hash: str) -> Job:
        try:
            query = self.session.query(Job)
            entity = query \
                .filter(Job.hash == unique_hash) \
                .one()
            return self.convert(entity)
        except MultipleResultsFound as e:
            raise EntityNotFoundException("Job id is not unique!", e)
        except NoResultFound as e:
            raise EntityNotFoundException("Job was not found in database!", e)
        except Exception as e:
            raise DataAccessException("Failed to edit job in database!", e)

    def get_next_free(self) -> Job:
        try:
            query = self.session.query(Job)
            entity = query \
                .order_by(asc(Job.date_added)) \
                .filter(Job.locked == False) \
                .first()
            return self.convert(entity)
        except NoResultFound as e:
            raise EntityNotFoundException("Job was not found in database!", e)
        except Exception as e:
            raise DataAccessException("Failed to edit job in database!", e)

    def get_next_free_in_plugin_list(self, plugin_list: List[str]) -> Job:
        try:
            query = self.session.query(Job)
            entity = query \
                .order_by(asc(Job.date_added)) \
                .filter(and_(Job.locked == False, Job.plugin in plugin_list)) \
                .first()
            return self.convert(entity)
        except NoResultFound as e:
            raise EntityNotFoundException("Job was not found in database!", e)
        except Exception as e:
            raise DataAccessException("Failed to edit job in database!", e)

    def lock(self, job_id: UUID) -> None:
        try:
            query = self.session.query(Job)
            entity = query \
                .filter(Job.id == job_id) \
                .one()
            entity.locked = True
        except MultipleResultsFound as e:
            raise EntityNotFoundException("Job id is not unique!", e)
        except NoResultFound as e:
            raise EntityNotFoundException("Job was not found in database!", e)
        except Exception as e:
            raise DataAccessException("Failed to edit job in database!", e)

    def unlock(self, job_id: UUID) -> None:
        try:
            query = self.session.query(Job)
            entity = query \
                .filter(Job.id == job_id) \
                .one()
            entity.locked = False
        except MultipleResultsFound as e:
            raise EntityNotFoundException("Job id is not unique!", e)
        except NoResultFound as e:
            raise EntityNotFoundException("Job was not found in database!", e)
        except Exception as e:
            raise DataAccessException("Failed to edit job in database!", e)
