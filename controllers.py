from bs4 import BeautifulSoup
import requests

from database import DatabaseConnect
from models import Book


class Parser:
    BASE = "https://www.dut.edu.ua"

    @staticmethod
    def start(url):
        links_to_selections = Parser.get_links_to_selections(url)

        links_to_sections_within_section = []
        for link_from_selection in links_to_selections:
            links_to_sections_within_section = Parser.get_links_to_sections_within_section(link_from_selection)

            list_of_links_to_books_by_section = []
            for links in links_to_sections_within_section:
                list_of_links_to_books_by_section = Parser.get_list_of_links_to_books_by_section(links)

                for links_on_book in list_of_links_to_books_by_section:
                    print(links_on_book)
                    Parser.inset_book_to_db(links_on_book)

        # list_of_links_to_books_by_section = Parser.get_list_of_links_to_books_by_section(
        #     links_to_sections_within_section[0])
        #
        # print(links_to_sections_within_section[0])
        # for i in list_of_links_to_books_by_section:
        #     print(i)
        #     Parser.inset_book_to_db(i)

    @staticmethod
    def get_links_to_selections(url):
        req = requests.get(url)
        soup = BeautifulSoup(req.content, "html.parser")
        links_to_sections = []

        for i in soup.select(".sub_pages_full_list_ul"):
            for link in i.findAll('a'):
                links_to_sections.append(Parser.BASE + link.get('href'))

        return links_to_sections

    @staticmethod
    def get_links_to_sections_within_section(url):
        links_to_sections_within_section = []
        req = requests.get(url)
        soup = BeautifulSoup(req.content, "html.parser")

        for i in soup.select(".sub_pages_main_menu_items"):
            link = str(i.get('onclick')).replace('document.location.href="', "https://www.dut.edu.ua")
            links_to_sections_within_section.append(link[:-1])

        return links_to_sections_within_section

    @staticmethod
    def get_list_of_links_to_books_by_section(url):
        list_links_to_books = []

        req = requests.get(url)
        soup = BeautifulSoup(req.content, "html.parser")

        for i in soup.select(".news_index_title"):
            for link in i.findAll('a'):
                list_links_to_books.append(Parser.BASE + link.get('href'))

        return list_links_to_books

    @staticmethod
    def inset_book_to_db(url):
        req = requests.get(url)
        soup = BeautifulSoup(req.content, "html.parser")

        title = soup.select('.content_title')[0].text
        dict_left_right_details = {}

        for i in soup.select(".lib_details"):
            dict_left_right_details = {
                "Автор: ": None,
                "Мова документу: ": None,
                "Розмір документу: ": None,
                "Рік публікації: ": None,
                "Видавництво: ": None,
                "Країна, місто: ": None,
                "Кількість сторінок: ": None,
                "Наявність у бібліотеці: ": None,
                "Наявність в електронному вигляді: ": None,
                "Створено: ": None,
                "Категорія: ": None,
                "Тип документу: ": None,
                "link_to_book": None
            }

            left = i.select('.lib_details_left')
            right = i.select('.lib_details_right')

            for j in range(len(right)):
                dict_left_right_details[str(left[j].text)] = str(right[j].text)

        # print(dict_left_right_details)

        book = Book(title)
        book.author = dict_left_right_details['Автор: ']
        book.lang = dict_left_right_details['Мова документу: ']
        book.document_size = dict_left_right_details['Розмір документу: ']
        book.year_of_publication = dict_left_right_details['Рік публікації: ']
        book.publishing_house = dict_left_right_details['Видавництво: ']
        book.country = dict_left_right_details['Країна, місто: ']
        book.number_of_pages = dict_left_right_details['Кількість сторінок: ']
        book.availability_in_the_library = dict_left_right_details['Наявність у бібліотеці: ']
        book.availability_in_electronic_form = dict_left_right_details['Наявність в електронному вигляді: ']
        book.added = dict_left_right_details['Створено: ']
        book.classification = dict_left_right_details['Категорія: ']
        book.document_type = dict_left_right_details['Тип документу: ']

        try:
            book.link_to_book = Parser.BASE + soup.select('.file')[0].find("a").get('href')
            print(book.link_to_book)
            DatabaseConnect.insert(book)
        except Exception as _ex:
            print("[INFO] This book has no references!")
