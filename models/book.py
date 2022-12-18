class Book:

    def __init__(self, title):
        self.id = None
        self.title = title

    @classmethod
    def create_book(cls, id, title, author, lang, document_size, year_of_publication, publishing_house, country,
                    number_of_pages, availability_in_the_library,availability_in_electronic_form, added,
                    classification_id, document_type, link, sub_category, global_category):
        book = cls(title)
        book.id = id
        book.title = title
        book.author = author
        book.lang = lang
        book.document_size = document_size
        book.year_of_publication = year_of_publication
        book.publishing_house = publishing_house
        book.country = country
        book.number_of_pages = number_of_pages
        book.availability_in_the_library = availability_in_the_library
        book.availability_in_electronic_form = availability_in_electronic_form
        book.added = added
        book.classification_id = classification_id
        book.document_type = document_type
        book.link = link
        book.sub_category = sub_category
        book.global_category = global_category
        return book

