import math
from typing import List
from models.book import Book


class SearchResult:
    def __init__(self, books: List[Book], search_query_id: int):
        self.data = books
        self.search_query_id = search_query_id
        self.data_length = len(books)


class PagesResult:
    def __init__(self, result: SearchResult, results_per_page: int = 3):
        self.result = result
        self.results_per_page = results_per_page

    def get_page(self, index: int):
        page = self.result.data[index * self.results_per_page: (index + 1) * self.results_per_page]
        return page

    def get_total_pages_count(self):
        return math.ceil(self.result.data_length / self.results_per_page)
