class Book:
    def __init__(self, title):
        self.title = title

    @classmethod
    def create_book(cls, id, title, author, lang, document_size, year_of_publication, publishing_house, country,
                    number_of_pages, availability_in_the_library,
                    availability_in_electronic_form, added, classification, document_type, link):
        cls.id = id
        cls.title = title
        cls.author = author
        cls.lang = lang
        cls.document_size = document_size
        cls.year_of_publication = year_of_publication
        cls.publishing_house = publishing_house
        cls.country = country
        cls.number_of_pages = number_of_pages
        cls.availability_in_the_library = availability_in_the_library
        cls.availability_in_electronic_form = availability_in_electronic_form
        cls.added = added
        cls.classification = classification
        cls.document_type = document_type
        cls.link = link

        return cls

    def __str__(self) -> str:
        return str(self.id) + " " + str(self.title) + " " + str(self.author)
