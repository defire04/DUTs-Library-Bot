from typing import List
from book import Book

class SearchResult:
    def __init__(self, books: List[Book], search_query: str):
        self.data = books
        self.search_query = search_query
        self.data_length = len(books)


class PagesResult:
    def __init__(self, result: SearchResult, results_per_page: int = 4):
        self.result = result
        self.results_per_page = results_per_page

    def get_page(self, index: int):
        page = self.result.data[index *
                                self.results_per_page: (index + 1) * self.results_per_page]
        return page