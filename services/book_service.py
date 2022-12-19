
import psycopg2

from resources.config import host, username, password, datasource



class BookService:
    connection = psycopg2.connect(host=host, user=username, password=password, database=datasource)
    cursor = connection.cursor()

    @staticmethod
    def insert(book):
        sql = """INSERT INTO books (title, author, lang, document_size, year_of_publication, publishing_house, 
        country, number_of_pages, availability_in_the_library, availability_in_electronic_form, added, 
        classification_id, document_type, link_to_book, sub_category, global_category) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
        record_to_insert = (
            book.title, book.author, book.lang, book.document_size, book.year_of_publication, book.publishing_house,
            book.country, book.number_of_pages, book.availability_in_the_library, book.availability_in_electronic_form,
            book.added, book.classification_id, book.document_type, book.link, book.sub_category, book.global_category)
        BookService.cursor.execute(sql, record_to_insert)
        BookService.connection.commit()


    @staticmethod
    def find_by_title(title):
        like_title = """ '%""" + title + """%';"""
        sql = """SELECT * FROM books WHERE LOWER(title) LIKE""" + like_title.lower()

        print(sql)
        BookService.cursor.execute(sql)
        return BookService.cursor.fetchall()

    @staticmethod
    def find_book_by_ids(request_books: str):
        request_books = request_books.replace(" ", ", ")
        sql = """SELECT * FROM books WHERE id in (""" + request_books + """)"""
        BookService.cursor.execute(sql)

        return BookService.cursor.fetchall()

    @staticmethod
    def find_books_by_book_category(category_id):
        sql = """SELECT * FROM books WHERE classification_id = %s"""
        BookService.cursor.execute(sql, (category_id,))

        return BookService.cursor.fetchall()



    @staticmethod
    def replace_c():
        sql_select = """UPDATE books SET title = REPLACE(title ,'С++', 'C++' ) WHERE title LIKE '%С++%';
                        UPDATE books SET title = REPLACE(title ,'С#', 'C#' ) WHERE title LIKE '%С#%';"""
        BookService.cursor.execute(sql_select)
        BookService.connection.commit()

    @staticmethod
    def clean_dataset():
        sql_drop = "TRUNCATE TABLE books;"
        BookService.cursor.execute(sql_drop)
        BookService.connection.commit()

    @staticmethod
    def finalize():
        BookService.cursor.close()
        BookService.connection.close()
        print("Database connection dead!")
