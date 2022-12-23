from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ContentType

from controllers.book_controller import BookController
from controllers.keyboard_controller import KeyboardController
from controllers.message_controller import MessageController
from controllers.query_controller import QueryController
from controllers.user_controller import UserController
from models.search_result import PagesResult, SearchResult
from models.user import User

from resources.config import TOKEN

from actions.action_creator import ButtonAction, ButtonPageAction, Actions, ButtonPageActionPayload
from controllers.library_controller import LibraryController

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

action = ButtonPageAction(1, 2)
button = InlineKeyboardButton('Text', callback_data=action.stringify())
inline_kb_full = InlineKeyboardMarkup(row_width=2).add(button)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nНапиши мне название книги!\nЗапрос должен содержать минимум 3 символа!")


def get_search_result_from_search_query(search_string: str):
    book_list_and_query = BookController.find_by_title_and_create_query(search_string)

    if not book_list_and_query["books"]:
        return None

    return SearchResult(book_list_and_query["books"], book_list_and_query["query_id"])


@dp.message_handler()
async def handel_find_book(msg: types.Message):
    add_new_user(msg.from_user.id, msg.from_user.username)

    if len(msg.text) < 2:
        await bot.send_message(msg.from_user.id, "Запрос должен содержать минимум 2 символа!")
        return

    search_result = get_search_result_from_search_query(msg.text)
    pages = PagesResult(search_result)

    if not search_result:
        await bot.send_message(msg.from_user.id, "Такой книги нет или запрос не верен!")
        return

    page_index = 0

    keyboard = KeyboardController.create_pages_keyboard(pages, page_index)

    message = MessageController.preapare_page_message(pages.get_page(page_index))

    await bot.send_message(msg.from_user.id, message, reply_markup=keyboard, parse_mode="html")
    await msg.delete()


@dp.callback_query_handler(
    lambda callback: callback.data and ButtonAction.from_json(callback.data).id == Actions.SWITCH_PAGE)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    action = ButtonAction[ButtonPageActionPayload].from_json(callback_query.data)
    page_index = action.payload.page_index
    query_id = action.payload.prepared_collection_id

    books = LibraryController.find_books_by_query_id(query_id)

    search_result = SearchResult(books, query_id)
    pages = PagesResult(search_result)
    message = callback_query.message

    keyboard = KeyboardController.create_pages_keyboard(pages, page_index)

    message_text = MessageController.preapare_page_message(pages.get_page(page_index))
    await message.edit_text(message_text, parse_mode="html")
    await message.edit_reply_markup(keyboard)


@dp.message_handler(content_types=ContentType.ANY)
async def unknown_type_of_message(msg: types.Message):
    add_new_user(msg.from_user.id, msg.from_user.username)

    await bot.send_sticker(chat_id=msg.from_user.id,
                           sticker=r"CAACAgIAAxkBAAEG6K9jocRBRnn3HykoJBwDzHVxv3FN5wACEgADbrttNcV0uCSF9fevLAQ")


def add_new_user(user_id, username):
    if not UserController.check_is_user_in_db(user_id):
        user = User(user_id, username)
        UserController.insert(user)


def start():
    executor.start_polling(dp)
    BookController.finalize()
    QueryController.finalize()
