class SearchCriteria:
    def __init__(self, field: str, term: str, weight: int = 1) -> None:
        super().__init__()
        self.field = field
        self.weight = weight
        self.term = term
