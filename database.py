
class DatabaseConnect:

    # connection = psycopg2.connect(host=host, user=username, password=password, database=datasource)
    # cursor = connection.cursor()


    @staticmethod
    def insert(book):
        print(book)
        # sql = """INSERT INTO books (title, author, lang, document_size, year_of_publication, publishing_house, country, 
        # number_of_pages, availability_in_the_library, availability_in_electronic_form, added, classification, document_type, link_to_book)
        #  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        # record_to_insert = (book.title, book.author, book.lang, book.document_size, book.year_of_publication, book.publishing_house, book.country, book.number_of_pages,
        #                     book.availability_in_the_library, book.availability_in_electronic_form, book.added, book.classification, book.document_type, book.link_to_book)
        # DatabaseConnect.cursor.execute(sql, record_to_insert)
        # DatabaseConnect.connection.commit()


