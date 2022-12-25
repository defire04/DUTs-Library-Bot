class Category:

    def __init__(self, id: int, title: str):
        self.id = id
        self.title = title


class CategoriesEnum:
    GLOBAL = 0
    SUB = 1
    BOOK = 2
