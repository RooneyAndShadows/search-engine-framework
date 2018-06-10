import sys


class RangeCriteria:
    def __init__(self, field: str, minimum: str = 0, maximum: str = str(sys.maxsize)):
        self.field = field
        self.minimum = minimum
        self.maximum = maximum
