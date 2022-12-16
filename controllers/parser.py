from bs4 import BeautifulSoup
import requests

from services.book_service import BookService
from models.book import Book
import time
from datetime import datetime
from multiprocessing import Pool

from util import util
from util.performance_counter import PerformanceCounter

process_counter = PerformanceCounter()
program_counter = PerformanceCounter()


class Parser:
    BASE = "https://www.dut.edu.ua"
    URL = "https://www.dut.edu.ua/ua/lib/1/category/2122"

    @staticmethod
    def start():
        print("Parser start!")

        program_counter.start()
        links_to_selections = Parser.get_links_to_selections(Parser.URL)

        links_to_sections_within_section = []
        list_of_links_to_books_by_section = []
        p = Pool(8)

        process_counter.start()
        links_to_sections_within_section.extend(
            util.merge_array_of_arrays(
                p.map(Parser.get_links_to_sections_within_section, links_to_selections)))
        process_counter.end()
        process_counter.printResult()

        process_counter.start()
        list_of_links_to_books_by_section.extend(
            util.merge_array_of_arrays(
                p.map(Parser.get_list_of_links_to_books_by_section, links_to_sections_within_section)))
        # print(list_of_links_to_books_by_section)
        process_counter.end()
        process_counter.printResult()

        process_counter.start()
        count_of_books = len(p.map(Parser.get_book_characteristics_and_insert_to_db,
                                   list_of_links_to_books_by_section))
        print('Count of books : ' + str(count_of_books))
        process_counter.end()
        process_counter.printResult()
        program_counter.end()

        print("Start:", datetime.fromtimestamp(program_counter.time_start))
        print("End:", datetime.fromtimestamp(time.time()))


        return program_counter.printResult()

    @staticmethod
    def get_book_characteristics_and_insert_to_db(link_on_book):
        # print(link_on_book)
        Parser.insert_book_to_db(
            Parser.get_dict_with_book_characteristics(link_on_book))
        return 1

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
            link = str(i.get('onclick')).replace(
                'document.location.href="', "https://www.dut.edu.ua")
            links_to_sections_within_section.append(link[:-1])

        temp_list_for_any_pages = []
        for i in links_to_sections_within_section:
            for any_links in Parser.check_are_there_any_pages_in_this_category(i):
                temp_list_for_any_pages.append(any_links)

        for any_links in temp_list_for_any_pages:
            links_to_sections_within_section.append(any_links)

        return links_to_sections_within_section

    @staticmethod
    def check_are_there_any_pages_in_this_category(url):
        req = requests.get(url)
        soup = BeautifulSoup(req.content, "html.parser")

        links_to_sections_within_section = []

        for j in soup.select(".pages_link"):
            for link in j.findAll('a'):
                if " »» " == link.text:
                    href = str(link.get('href'))
                    for_parse_number_of_pages = href.split("/")

                    for k in range(2, int(for_parse_number_of_pages[3]) + 1):
                        links_to_sections_within_section.append(
                            Parser.BASE + "/ua/lib/" + str(k) + href[9:])
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
    def get_dict_with_book_characteristics(url):
        req = requests.get(url)
        soup = BeautifulSoup(req.content, "html.parser")
        dict_with_book_characteristics = {}

        for i in soup.select(".lib_details"):
            dict_with_book_characteristics = {
                "title": None,
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

            dict_with_book_characteristics["title"] = soup.select('.content_title')[0].text
            for j in range(len(right)):
                dict_with_book_characteristics[str(
                    left[j].text)] = str(right[j].text)
            try:
                dict_with_book_characteristics["link_to_book"] = Parser.BASE + soup.select('.file')[0].find("a").get(
                    'href')
            except Exception as _ex:
                print("[INFO]" + dict_with_book_characteristics["title"] + " book has no references!")

        return dict_with_book_characteristics

    @staticmethod
    def insert_book_to_db(dict_with_book_characteristics):
        book = Book(dict_with_book_characteristics['title'])
        book.author = dict_with_book_characteristics['Автор: ']
        book.lang = dict_with_book_characteristics['Мова документу: ']
        book.document_size = dict_with_book_characteristics['Розмір документу: ']
        book.year_of_publication = dict_with_book_characteristics['Рік публікації: ']
        book.publishing_house = dict_with_book_characteristics['Видавництво: ']
        book.country = dict_with_book_characteristics['Країна, місто: ']
        book.number_of_pages = dict_with_book_characteristics['Кількість сторінок: ']
        book.availability_in_the_library = dict_with_book_characteristics[
            'Наявність у бібліотеці: ']
        book.availability_in_electronic_form = dict_with_book_characteristics[
            'Наявність в електронному вигляді: ']
        book.added = dict_with_book_characteristics['Створено: ']
        book.classification = dict_with_book_characteristics['Категорія: ']
        book.document_type = dict_with_book_characteristics['Тип документу: ']
        book.link = dict_with_book_characteristics['link_to_book']

        BookService.insert(book)