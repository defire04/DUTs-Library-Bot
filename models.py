
class Book:

    def __init__(self, title):
        self.title = title

    def __init__(self, id, title, author, lang, document_size, year_of_publication, publishing_house, country,
                 number_of_pages, availability_in_the_library,
                 availability_in_electronic_form, added, classification, document_type, link):
        self.id = id
        self.title = title
        self.author = author
        self.lang = lang
        self.document_size = document_size
        self.year_of_publication = year_of_publication
        self.publishing_house = publishing_house
        self.country = country
        self.number_of_pages = number_of_pages
        self.availability_in_the_library = availability_in_the_library
        self.availability_in_electronic_form = availability_in_electronic_form
        self.added = added
        self.classification = classification
        self.document_type = document_type
        self.link = link

    def __str__(self) -> str:
        return str(self.id) + " " + str(self.title) + " " + str(self.author)

# 332 Изучаем C# Э. Стиллмен, Д. Грин
# 348 C# 4.0 Полное руководство Шилдт Г.
# 397 C# 2005 для чайников Стефан Рэнди Дэвис, Чак Сфер
# 1112 C# 2005 для чайников Стефан Рэнди Дэвис, Чак Сфер
# SELECT * FROM books WHERE LOWER(title) LIKE '%c#%';

# 384 С#. Концепція та синтаксис. Навчальний посібник Голуб Б.М.