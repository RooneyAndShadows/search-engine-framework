from datetime import datetime, timedelta
from uuid import UUID

from core.src.crawler.server.dependency.service import hash_generator
from core.src.crawler.server.manager.base.BaseManager import BaseManager
from interfaces.src.base.exception.BasicException import BasicException
from interfaces.src.crawler.communication.common.JobDescription import JobDescription
from interfaces.src.crawler.communication.request.JobResult import JobResult
from interfaces.src.crawler.communication.response.BaseResponse import BaseResponse
from interfaces.src.crawler.communication.response.Error import Error
from interfaces.src.crawler.communication.response.JobInformation import JobInformation
from interfaces.src.crawler.server.data.data.JobData import JobData
from interfaces.src.crawler.server.data.exception.EntityNotFoundException import EntityNotFoundException
from interfaces.src.crawler.server.manager.IJobScheduler import IJobScheduler


class JobScheduler(BaseManager, IJobScheduler):
    def get_next_job(self, crawler_id: UUID) -> JobInformation:
        response = JobInformation()
        self.context.start_transaction()
        try:
            self.context.crawler_set().register_call(crawler_id)
            try:
                job = self.context.job_set().get_next_free()
            except EntityNotFoundException:
                self.context.save()
                self.context.commit()
                response.set_error(Error('ObjectNotFound', 404, 'No free jobs at the moment!'))
                return response
            self.context.job_set().lock(job.job_id)
            self.context.save()
            self.context.commit()
            response = JobInformation(JobDescription(job.type, job.target))
        except EntityNotFoundException as e:
            self.context.rollback()
            response.set_error(Error('ObjectNotFound', 404, e.message))
            return response
        except BasicException as e:
            self.context.rollback()
            response.set_error(Error("InternalServerError", 500, e.message))
        except Exception as e:
            self.context.rollback()
            response.set_error(Error("InternalServerError", 500, 'Unknown error occurred!'))
        return response

    def finish_job(self, crawler_id: UUID, result: JobResult) -> BaseResponse:
        response = BaseResponse()
        self.context.start_transaction()
        try:
            self.context.crawler_set().register_call(crawler_id)
            self.repository.finish_job(result.job_id, crawler_id)
            for job in result.job_list:
                unique_hash = hash_generator().generate_target_hash(job.target)
                try:
                    existing_job = self.context.job_set().get_by_hash(unique_hash)
                    expire_date = existing_job.date_added + timedelta(days=7)
                    if expire_date < datetime.now() and existing_job.locked:
                        self.context.job_set().unlock(existing_job.job_id)
                except EntityNotFoundException:
                    new_job = JobData(job.job_type, job.target, False, crawler_id)
                    self.context.job_set().add(new_job)
            self.context.save()
            self.context.commit()
            response = BaseResponse(True)
        except EntityNotFoundException as e:
            self.context.rollback()
            response.set_error(Error('ObjectNotFound', 404, e.message))
            return response
        except BasicException as e:
            self.context.rollback()
            response.set_error(Error("InternalServerError", 500, e.message))
        except Exception as e:
            self.context.rollback()
            response.set_error(Error("InternalServerError", 500, 'Unknown error occurred!'))
        return response
