from sqlalchemy.orm.session import Session


class BaseSet:
    def __init__(self, session: Session) -> None:
        self.session = session

