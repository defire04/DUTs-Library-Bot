from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from controllers.parser import Parser
from models.search_result import PagesResult, SearchResult
from resources.config import TOKEN
from services.book_service import BookService
from actions.action_creator import ButtonAction, ButtonPageAction, Actions
from services.query_servise import QueryService
from util.util import string_trim

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

action = ButtonPageAction(1, 2)
button = InlineKeyboardButton('Text', callback_data=action.stringify())
inline_kb_full = InlineKeyboardMarkup(row_width=2).add(button)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nНапиши мне название книги!\nЗапрос должен содержать минимум 3 символа!",
                        reply_markup=inline_kb_full)


def get_search_result_from_search_query(search_string: str):
    book_list_and_query = BookService.find_by_title_and_create_query(search_string)

    if not book_list_and_query["books"]:
        return None

    print(book_list_and_query["query_id"])
    return SearchResult(book_list_and_query["books"], book_list_and_query["query_id"])


@dp.message_handler()
async def echo_message(msg: types.Message):
    # print(msg.from_user.id)
    # print(msg.from_user.username)
    if len(msg.text) < 2:
        await bot.send_message(msg.from_user.id, "Запрос должен содержать минимум 2 символа!")
        return

    search_result = get_search_result_from_search_query(msg.text)

    pages = PagesResult(search_result)

    if not pages:
        await bot.send_message(msg.from_user.id, "Такой книги нет или запрос не верен!")
        return
    books_strings = []

    action_for_next_button = ButtonPageAction(1, int(search_result.search_query))
    next_button = InlineKeyboardButton('Text', callback_data=action_for_next_button.stringify())
    inline_kb_full = InlineKeyboardMarkup(row_width=1).add(next_button)

    for book in pages.get_page(0):
        books_strings.append("Название книги: " + string_trim(str(book.title)) + "\n"
                             "Id в бд: " + str(book.id) + "\n"
                             "Автор: " + string_trim(str(book.author)) + "\n"
                             "Год публикации: " + str(book.year_of_publication) + "\n"
                             "Ссылка: " + str(book.link) + "\n")

    await bot.send_message(msg.from_user.id, "\n".join(books_strings), reply_markup=inline_kb_full)


@dp.callback_query_handler(lambda callback: callback.data and ButtonAction.from_json(callback.data)
                           .id == Actions.SWITCH_PAGE)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    action = ButtonAction.from_json(callback_query.data)
    print(action.payload.page_index)
    print(action.payload.prepared_collection_id)

    print(QueryService.find_by_id(action.payload.prepared_collection_id).string_books_id)
    await bot.answer_callback_query(callback_query.id, text='Я хочу страницу ' + str(
        action.payload.page_index) + ' из запроса под id: ' + str(action.payload.prepared_collection_id))


if __name__ == '__main__':
    executor.start_polling(dp)
    BookService.finalize()
    QueryService.finalize()