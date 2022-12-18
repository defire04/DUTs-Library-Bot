class Book:

    def __init__(self, title):
        self.id = None
        self.title = title

    @classmethod
    def create_book(cls, id, title, author, lang, document_size, year_of_publication, publishing_house, country,
                    number_of_pages, availability_in_the_library,availability_in_electronic_form, added, classification,
                    document_type, link, sub_category, global_category):
        peremennay = cls(title)
        peremennay.id = id
        peremennay.title = title
        peremennay.author = author
        peremennay.lang = lang
        peremennay.document_size = document_size
        peremennay.year_of_publication = year_of_publication
        peremennay.publishing_house = publishing_house
        peremennay.country = country
        peremennay.number_of_pages = number_of_pages
        peremennay.availability_in_the_library = availability_in_the_library
        peremennay.availability_in_electronic_form = availability_in_electronic_form
        peremennay.added = added
        peremennay.classification = classification
        peremennay.document_type = document_type
        peremennay.link = link
        peremennay.sub_category = sub_category
        peremennay.global_category = global_category
        return peremennay

    # def __init__(self, id, title, author, lang, document_size, year_of_publication, publishing_house, country,
    #              number_of_pages, availability_in_the_library,
    #              availability_in_electronic_form, added, classification, document_type, link):
    #     self.id = id
    #     self.title = title
    #     self.author = author
    #     self.lang = lang
    #     self.document_size = document_size
    #     self.year_of_publication = year_of_publication
    #     self.publishing_house = publishing_house
    #     self.country = country
    #     self.number_of_pages = number_of_pages
    #     self.availability_in_the_library = availability_in_the_library
    #     self.availability_in_electronic_form = availability_in_electronic_form
    #     self.added = added
    #     self.classification = classification
    #     self.document_type = document_type
    #     self.link = link

    def __str__(self) -> str:
        return str(self.id) + " " + str(self.title) + " " + str(self.author)
