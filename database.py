import psycopg2
from config import host, username, password, datasource
from models import Book


class DatabaseConnect:
    connection = psycopg2.connect(
        host=host, user=username, password=password, database=datasource)
    cursor = connection.cursor()

    @staticmethod
    def insert(book):

        sql = """INSERT INTO books (title, author, lang, document_size, year_of_publication, publishing_house, 
        country, number_of_pages, availability_in_the_library, availability_in_electronic_form, added, 
        classification, document_type, link_to_book) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
        record_to_insert = (
            book.title, book.author, book.lang, book.document_size, book.year_of_publication, book.publishing_house,
            book.country, book.number_of_pages, book.availability_in_the_library, book.availability_in_electronic_form,
            book.added, book.classification, book.document_type, book.link_to_book)
        DatabaseConnect.cursor.execute(sql, record_to_insert)
        DatabaseConnect.connection.commit()

    @staticmethod
    def find_by_title(title):
        like_title = """ '%""" + title + """%';"""
        sql = """SELECT * FROM books WHERE title LIKE""" + like_title

        print(sql)
        DatabaseConnect.cursor.execute(sql)
        books = DatabaseConnect.cursor.fetchall()

        b2Test = Book(books[0][1], books[0][2], books[0][3], books[0][4], books[0][5], books[0][6],
                      books[0][7], books[0][8], books[0][9], books[0][10], books[0][11], books[0][12],
                      books[0][13], books[0][14])
        print(b2Test)

        print(len(books))
        return books

    @staticmethod
    def finalize():
        DatabaseConnect.cursor.close()
        DatabaseConnect.connection.close()
        print("Database connection dead!")
