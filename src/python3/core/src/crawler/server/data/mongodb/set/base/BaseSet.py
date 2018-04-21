from pymongo.database import Database


class BaseSet:
    def __init__(self, database: Database) -> None:
        self.database = database
