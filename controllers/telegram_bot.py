from typing import List

from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ContentType, Message
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from controllers.book_controller import BookController
from controllers.category_controller import CategoryController
from controllers.keyboard_controller import KeyboardController
from controllers.message_controller import MessageController
from controllers.query_controller import QueryController
from controllers.user_controller import UserController
from models.search_result import PagesResult, SearchResult
from models.user import User

from resources.config import TOKEN, admin1_id

from actions.action_creator import ButtonAction, ButtonPageAction, Actions, ButtonPageActionPayload
from controllers.library_controller import LibraryController

storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)
ADMINS = [admin1_id]

action = ButtonPageAction(1, 2)
button = InlineKeyboardButton('Text', callback_data=action.stringify())
inline_kb_full = InlineKeyboardMarkup(row_width=2).add(button)

admin_buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
admin_buttons.add("Рассылка")
admin_buttons.add("Пользователи")
admin_buttons.add("Найти книгу по названию!")

user_buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
user_buttons.add("Найти книгу по названию!")

back_buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
back_buttons.add(types.InlineKeyboardButton(text="Назад"))


class Dialog(StatesGroup):
    spam = State()
    users = State()
    search_books = State()


@dp.message_handler(commands=['start'])
async def process_start_command(msg: types.Message):
    add_new_user(msg)
    for admin_id in ADMINS:
        if msg.from_user.id == admin_id:
            await msg.answer('Добро пожаловать в Админ-Панель! Выберите действие на клавиатуре',
                             reply_markup=admin_buttons)
        else:
            await msg.reply("Добро пожаловать в DUT Library!\nВыберите в меню как вы хотите искать\n",
                            reply_markup=user_buttons)


@dp.message_handler(content_types=['text'], text='Пользователи')
async def get_users_for_admin(msg: types.Message):
    users: List[User] = []
    for admin_id in ADMINS:
        if msg.from_user.id == admin_id:
            users = UserController.get_users()
            break

    message_text = MessageController.prepare_page_message_for_users(users)
    await bot.send_message(msg.from_user.id, message_text)
    await msg.delete()


@dp.message_handler(content_types=ContentType.ANY, text='Рассылка')
async def spam(msg: types.Message):
    for admin_id in ADMINS:
        if msg.from_user.id == admin_id:
            await msg.answer('Напишите текст рассылки', reply_markup=back_buttons)
            await Dialog.spam.set()
        else:
            await msg.answer('Вы не являетесь админом')


@dp.message_handler(state=Dialog.spam)
async def start_spam(msg: types.Message, state: FSMContext):
    if msg.text == 'Назад':
        for admin_id in ADMINS:
            if admin_id == msg.from_user.id:
                await msg.answer('Главное меню', reply_markup=admin_buttons)
            else:
                await msg.answer('Главное меню', reply_markup=user_buttons)

        await state.finish()
    else:
        for user in UserController.get_users():
            for admin_id in ADMINS:
                if user.user_id != admin_id:
                    # await bot.send_photo(user.user_id, msg.photo)
                    await bot.send_message(user.user_id, msg.text)

        await msg.answer('Рассылка завершена')
        await state.finish()


def get_search_result_from_search_query(search_string: str):
    book_list_and_query = BookController.find_by_title_and_create_query(search_string)

    if not book_list_and_query["books"]:
        return None

    return SearchResult(book_list_and_query["books"], book_list_and_query["query_id"])


@dp.message_handler(content_types=['text'], text='Найти книгу по названию!')
async def start_find_books_by_title(msg: types.Message):
    await msg.answer('Напишите название книги. (Например: С++)', reply_markup=back_buttons)
    await Dialog.search_books.set()


@dp.message_handler(state=Dialog.search_books)
async def handel_find_book(msg: types.Message, state: FSMContext):
    if msg.text == 'Назад':
        for admin_id in ADMINS:
            if admin_id == msg.from_user.id:
                await msg.answer('Главное меню', reply_markup=admin_buttons)
            else:
                await msg.answer('Главное меню', reply_markup=user_buttons)

        await state.finish()

    else:
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

        message = MessageController.prepare_page_message(pages.get_page(page_index))

        await bot.send_message(msg.from_user.id, message, reply_markup=keyboard, parse_mode="html")
        await msg.delete()
        # TODO тут проблема
        await state.finish()

        for admin_id in ADMINS:
            if admin_id == msg.from_user.id:

                await msg.answer("Главное меню ", reply_markup=admin_buttons)
            else:
                await msg.answer("Главное меню", reply_markup=user_buttons)


@dp.message_handler(state='*', text='Назад')
async def back(msg: Message):
    for admin_id in ADMINS:
        if msg.from_user.id == admin_id:
            await msg.answer('Главное меню', reply_markup=admin_buttons)
        else:
            await msg.answer('Вы вернулись в главное меню', reply_markup=user_buttons)


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

    message_text = MessageController.prepare_page_message(pages.get_page(page_index))
    await message.edit_text(message_text, parse_mode="html")
    await message.edit_reply_markup(keyboard)


@dp.message_handler(content_types=ContentType.ANY)
async def unknown_type_of_message(msg: types.Message):
    await bot.send_sticker(chat_id=msg.from_user.id,
                           sticker=r"CAACAgIAAxkBAAEG6K9jocRBRnn3HykoJBwDzHVxv3FN5wACEgADbrttNcV0uCSF9fevLAQ")


def add_new_user(user_message: types.Message):
    if not UserController.check_is_user_in_db(user_message.from_user.id):
        user = User(user_message.from_user.id, user_message.from_user.username, user_message.from_user.full_name)
        UserController.insert(user)


def start():
    executor.start_polling(dp)
    BookController.finalize()
    QueryController.finalize()
    CategoryController.finalize()
    UserController.finalize()
