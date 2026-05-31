from math import ceil


class Pagination:

    def __init__(self, skip: int = 0, limit: int = 100):
        self.skip = max(0, skip)
        self.limit = max(1, min(limit, 1000))

    @property
    def page(self) -> int:
        return (self.skip // self.limit) + 1

    @staticmethod
    def calculate_total_pages(total: int, limit: int) -> int:
        return ceil(total / limit) if limit > 0 else 0


def paginate_query(skip: int = 0, limit: int = 100) -> tuple[int, int]:
    skip = max(0, skip)
    limit = min(max(1, limit), 1000)
    return skip, limit
