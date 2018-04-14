import pprint
import uuid
from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError

from core.src.crawler.server.data.sqlalchemy.SearchEngineContext import SearchEngineContext
from interfaces.src.crawler.enum.JobType import JobType
from interfaces.src.crawler.server.data.data.JobData import JobData

with SearchEngineContext("postgresql+psycopg2://postgres:_mk123_@localhost:5432/crawler_test") as context:
    c_id = UUID("5a84baf2-8ea8-4481-8809-027589255f81")
    has = context.crawler_set().exists(c_id)
    pprint.pprint(has)
    crawler = context.crawler_set().get(c_id)
    pprint.pprint(vars(crawler))
    try:
        context.crawler_set().register_call(c_id)
        context.commit()
    except SQLAlchemyError:
        context.rollback()
    crawler = context.crawler_set().get(c_id)
    pprint.pprint(vars(crawler))

    job = JobData(JobType.HARVEST, uuid.uuid4().hex, False, c_id)
    try:
        j_id = context.job_set().add(job)
        pprint.pprint(j_id)
        context.save()

        job = context.job_set().get(j_id)
        pprint.pprint(vars(job))
        context.commit()
    except SQLAlchemyError as exp:
        print(exp)
        context.rollback()

    job = context.job_set().get_next_free()
    pprint.pprint(vars(job))


