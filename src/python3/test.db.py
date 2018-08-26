import pprint
import uuid
from uuid import UUID

from easy_search.core.server.job.data.mongodb.SearchEngineContext import SearchEngineContext as MongoContext
from easy_search.interfaces.base.enum.JobType import JobType
from easy_search.interfaces.server.job.data.data.JobData import JobData

#with SQLAlchemyContext("postgresql+psycopg2://postgres:_mk123_@localhost:5432/crawler_test") as context:
with MongoContext("mongodb+srv://administrator:admin@easyserachdemo-edqtm.mongodb.net/test?retryWrites=true",
                  "carstorage") as context:
    c_id = UUID("5a84baf2-8ea8-4481-8809-027589255f81")
    has = context.crawler_set().exists(c_id)
    pprint.pprint(has)
    crawler = context.crawler_set().get(c_id)
    pprint.pprint(vars(crawler))
    try:
        context.crawler_set().register_call(c_id)
        context.commit()
    except Exception:
        context.rollback()
    crawler = context.crawler_set().get(c_id)
    pprint.pprint(vars(crawler))

    job = JobData(JobType.HARVEST, 'https://www.cars.bg/?go=cars&search=1&advanced=&fromhomeu=1&currencyId=1&'
                                   'yearTo=&autotype=1&stateId=1&section=home&categoryId=0&doorId=0&brandId=0&'
                                   'modelId=0&fuelId=0&gearId=0&yearFrom=&priceFrom=&priceTo=&man_priceFrom=&'
                                   'man_priceTo=&regionId=0&offersFor4=1&offersFor1=1&filterOrderBy=1',
                  False, c_id, 'cars.bg')
    try:
        j_id = context.job_set().add(job)
        pprint.pprint(j_id)
        context.save()

        job = context.job_set().get(j_id)
        pprint.pprint(vars(job))
        context.commit()
    except Exception as exp:
        print(exp)
        context.rollback()

    job = context.job_set().get_next_free()
    pprint.pprint(vars(job))


