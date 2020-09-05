import uuid
from datetime import datetime
from typing import List
from uuid import UUID

import pymongo
from pymongo.collection import Collection

from easy_search.core.base.dependency.service import hash_generator
from easy_search.interfaces.base.enum.JobType import JobType
from .base.BaseSet import BaseSet
from easy_search.interfaces.server.job.data.data.JobData import JobData
from easy_search.interfaces.server.job.data.entity.Job import Job as JobDTO, Job
from easy_search.interfaces.server.job.data.exception.DataAccessException import DataAccessException
from easy_search.interfaces.server.job.data.exception.EntityNotFoundException import EntityNotFoundException
from easy_search.interfaces.server.job.data.set.IJobSet import IJobSet


class JobSet(BaseSet, IJobSet):

    def get_collection(self) -> Collection:
        return self.database.jobs

    def convert(self, entity) -> JobDTO:
        job = JobDTO(entity["job_id"], JobType(entity["type"]), entity["url"], entity["hash"], entity["locked"],
                     entity["date_added"], entity["crawler_id"], entity["plugin_type"], entity["repeat"],
                     entity["repeat_after"])
        if entity["done_by"] is not None:
            job.set_executor_crawler_id(entity["done_by"], entity["date_done"])
        return job

    def fill(self, data: JobData, job) -> None:
        job["date_done"] = data.date_executed
        job["done_by"] = data.executor_id.__str__()
        job["crawler_id"] = data.creator_id.__str__()
        job["locked"] = data.locked
        job["plugin_type"] = data.plugin_type
        job["hash"] = hash_generator().generate_target_hash(data.target)
        job["url"] = data.target
        job["type"] = data.type.value
        job["repeat"] = data.repeat
        job["repeat_after"] = data.repeat_after

    def add(self, job: JobData) -> UUID:
        try:
            entity = {}
            self.fill(job, entity)
            new_id = uuid.uuid4()
            entity["job_id"] = new_id.__str__()
            entity["date_added"] = datetime.now()
            self.get_collection().insert_one(entity)
            return new_id
        except Exception as e:
            raise DataAccessException("Failed to add job to database!", e)

    def edit(self, job_id: UUID, job: JobData) -> None:
        try:
            entity = self.get_collection().find_one({"job_id": job_id.__str__()})
            self.fill(job, entity)
            self.get_collection().find_one_and_update({"job_id": job_id.__str__()},
                                                      {"$set": entity})
        except Exception as e:
            raise DataAccessException("Failed to edit job in database!", e)

    def delete(self, job_id: UUID) -> None:
        try:
            self.get_collection().find_one_and_delete({"job_id": job_id.__str__()})
        except Exception as e:
            raise DataAccessException("Failed to delete job from database!", e)

    def get(self, job_id: UUID) -> JobDTO:
        try:
            entity = self.get_collection().find_one({"job_id": job_id.__str__()})
        except Exception as e:
            raise DataAccessException("Failed get job from database!", e)
        if entity is None:
            raise EntityNotFoundException("Job with id not found!")
        try:
            return self.convert(entity)
        except Exception as e:
            raise DataAccessException("Failed convert job from database!", e)

    def get_by_hash(self, unique_hash: str) -> JobDTO:
        try:
            entity = self.get_collection().find_one({"hash": unique_hash})
        except Exception as e:
            raise DataAccessException("Failed get job from database!", e)
        if entity is None:
            raise EntityNotFoundException("Job with hash not found!")
        try:
            return self.convert(entity)
        except Exception as e:
            raise DataAccessException("Failed convert job from database!", e)

    def get_next_free(self) -> JobDTO:
        try:
            entity = self.get_collection().find_one_and_update({"locked": False, 'date_done': None},
                                                               {"$set": {"locked": True}},
                                                               sort=[("date_added", pymongo.ASCENDING)])
            if entity is None:
                entity = self.get_collection().find_one_and_update(
                    {"locked": False,
                     'date_done': {"$ne": None}, 'repeat_after': {"$gte": datetime.now()}},
                    {"$set": {"locked": True}},
                    sort=[("repeat_after", pymongo.ASCENDING)])
        except Exception as e:
            raise DataAccessException("Failed get job from database!", e)
        if entity is None:
            raise EntityNotFoundException("No free jobs found!")
        try:
            return self.convert(entity)
        except Exception as e:
            raise DataAccessException("Failed convert job from database!", e)

    def get_next_free_in_plugin_list(self, plugin_list: List[str]) -> Job:
        try:
            entity = self.get_collection().find_one_and_update({"locked": False, "plugin_type": {"$in": plugin_list},
                                                                'date_done': None},
                                                               {"$set": {"locked": True}},
                                                               sort=[("date_added", pymongo.ASCENDING)])
            if entity is None:
                entity = self.get_collection().find_one_and_update(
                    {"locked": False,
                     'date_done': {"$ne": None}, 'repeat_after': {"$gte": datetime.now()}},
                    {"$set": {"locked": True}},
                    sort=[("repeat_after", pymongo.ASCENDING)])
        except Exception as e:
            raise DataAccessException("Failed get job from database!", e)
        if entity is None:
            raise EntityNotFoundException("No free jobs found!")
        try:
            return self.convert(entity)
        except Exception as e:
            raise DataAccessException("Failed convert job from database!", e)

    def lock(self, job_id: UUID) -> None:
        try:
            self.get_collection().find_one_and_update({"job_id": job_id.__str__()},
                                                      {"$set": {"locked": True}})
        except Exception as e:
            raise DataAccessException("Failed to edit job in database!", e)

    def unlock(self, job_id: UUID) -> None:
        try:
            self.get_collection().find_one_and_update({"job_id": job_id.__str__()},
                                                      {"$set": {"locked": False}})
        except Exception as e:
            raise DataAccessException("Failed to edit job in database!", e)
