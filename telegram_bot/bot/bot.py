from typing import List

from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ContentType, Message
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from controllers.category_controller import CategoryController
from controllers.query_controller import QueryController
from controllers.user_controller import UserController
from models.user import User

from resources.config import TOKEN, admins
from models.category import CategoriesEnum

from telegram_bot.actions.action_creator import ButtonPageActionPayload
from telegram_bot.controllers.library_controller import LibraryController
from telegram_bot.controllers.message_controller import MessageController

from telegram_bot.handlers.category_search_handlers import *
from telegram_bot.handlers.process_main_menu_command import process_main_menu_command
from telegram_bot.handlers.process_start_command import process_start_command
from telegram_bot.handlers.sort_direction_change_handler import sort_direction_change_handler
from telegram_bot.handlers.sort_field_change_handler import sort_field_change_handler

from util.filter_query_by_action import create_filter_query_by_action

storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)
ADMINS = admins

admin_buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
admin_buttons.add("Розсилка")
admin_buttons.add("Користувачі")
admin_buttons.add("Кількість користувачів")

user_buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
user_buttons.add("Найти книгу по названию!")

back_buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
back_buttons.add(types.InlineKeyboardButton(text="Назад"))

back_buttons_to_admin_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
back_buttons_to_admin_menu.add(types.InlineKeyboardButton(text="Назад до адмін меню"))


class Dialog(StatesGroup):
    spam = State()
    users = State()
    search_books = State()


dp.register_message_handler(commands=['start'], callback=process_start_command)
dp.register_message_handler(commands=['menu'], callback=process_main_menu_command)

dp.register_callback_query_handler(
    open_category_search_handler,
    create_filter_query_by_action(Actions.OPEN_CATEGORY_SEARCH)
)
dp.register_callback_query_handler(
    global_category_search_handler,
    create_filter_category_action_by_type(CategoriesEnum.GLOBAL)
)
dp.register_callback_query_handler(
    sub_category_search_handler,
    create_filter_category_action_by_type(CategoriesEnum.SUB)
)
dp.register_callback_query_handler(
    book_category_search_handler,
    create_filter_category_action_by_type(CategoriesEnum.BOOK)
)
dp.register_callback_query_handler(
    sort_direction_change_handler,
    create_filter_query_by_action(Actions.CHANGE_SORT_DIRECTION)
)
dp.register_callback_query_handler(
    sort_field_change_handler,
    create_filter_query_by_action(Actions.CHNAGE_SORT_FIELD)
)


@dp.callback_query_handler(create_filter_query_by_action(Actions.START_SEARCH))
async def handle_search(callback_querry: types.CallbackQuery):
    await callback_querry.message.delete()
    await Dialog.search_books.set()
    await callback_querry.message.answer(
        'Введіть назву книги (можна приблизно, наприклад: c++)\nЗапит повинен містити щонайменше 2 символи!',
        reply_markup=back_buttons)


@dp.callback_query_handler(create_filter_query_by_action(Actions.TO_MAIN_MENU))
async def handle_search_exit(callback_querry: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback_querry.message.answer(**Messages.main_menu_message.get_args())
    await callback_querry.message.delete()


@dp.message_handler(content_types=['text'], text='Користувачі')
async def get_users_for_admin(msg: types.Message):
    users: List[User] = []
    if msg.from_user.id in ADMINS:
        users = UserController.get_users()
    else:
        await msg.answer('Ви не є адміном!')

    message_text = MessageController.prepare_page_message_for_users(users)
    await bot.send_message(msg.from_user.id, message_text)
    await msg.delete()


@dp.message_handler(content_types=['text'], text='Кількість користувачів')
async def get_count_users_for_admin(msg: types.Message):
    users: List[User] = []

    if msg.from_user.id in ADMINS:
        users = UserController.get_users()
    else:
        await msg.answer('Ви не є адміном!')

    message_text = "Кількість користувачів за весь час: " + str(len(users))
    await bot.send_message(msg.from_user.id, message_text)
    await msg.delete()


@dp.message_handler(content_types=ContentType.ANY, text='Розсилка')
async def spam(msg: types.Message):
    if msg.from_user.id in ADMINS:
        await msg.answer('Напишіть текст розсилки', reply_markup=back_buttons_to_admin_menu)
        await Dialog.spam.set()
    else:
        await msg.answer('Ви не є адміном!')


@dp.message_handler(state=Dialog.spam)
async def start_spam(msg: types.Message, state: FSMContext):
    if msg.text == 'Назад до адмін меню':
        if msg.from_user.id in ADMINS:
            await msg.answer('Головне меню', reply_markup=admin_buttons)
        else:
            await KeyboardController.remove_inline_keyboard(msg)
            await msg.answer(**Messages.start_message.get_args())
        await state.finish()
    else:
        for user in UserController.get_users():
            if user.user_id not in ADMINS:
                # await bot.send_photo(user.user_id, msg.photo)
                await bot.send_message(user.user_id, msg.text)

        await msg.answer('Розсилка завершена', reply_markup=admin_buttons)
        await state.finish()


# @dp.message_handler(content_types=['text'], text='Знайти книгу за назвою!')
# async def start_find_books_by_title(msg: types.Message):
#     await msg.answer('Напишіть назву книги. (Наприклад: С++)', reply_markup=back_buttons)
#     await Dialog.search_books.set()


@dp.message_handler(state=Dialog.search_books)
async def handel_find_book(msg: types.Message, state: FSMContext):
    if msg.text == 'Назад':

        await KeyboardController.remove_inline_keyboard(msg)
        await msg.answer(**Messages.main_menu_message.get_args())

        await state.finish()

    else:
        if len(msg.text) < 2:
            await bot.send_message(msg.from_user.id, "Запит повинен містити щонайменше 2 символи!")
            return

        book_list_and_query = BookController.find_by_title_and_create_query(msg.text)

        if not book_list_and_query["books"]:
            await msg.answer(**Messages.no_book_message.get_args())
            return

        message_creator = MessageFabric.create_page_message(book_list_and_query["books"],
                                                            query_id=book_list_and_query["query_id"])

        await msg.answer(**message_creator.get_args())
        await state.finish()


@dp.message_handler(state='*', text='Назад')
async def back(msg: Message):
    await KeyboardController.remove_inline_keyboard(msg)
    await msg.answer(**Messages.start_message.get_args())


@dp.message_handler(commands=['give_my_admin'])
async def admin(msg: types.Message):
    if msg.from_user.id in ADMINS:
        await msg.answer("Ласкаво просимо до меню адміністратора!", reply_markup=admin_buttons)
    else:
        await msg.answer('Ви не є адміном!')


@dp.message_handler(state='*', text='Назад до адмін меню')
async def back_to_admin(msg: Message):
    await KeyboardController.remove_inline_keyboard(msg)

    if msg.from_user.id in ADMINS:
        await msg.answer("Головне меню адміна", reply_markup=admin_buttons)
    else:
        await msg.answer('Ви не є адміном!')


@dp.callback_query_handler(create_filter_query_by_action(Actions.SWITCH_PAGE))
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    action = ButtonAction[ButtonPageActionPayload].from_json(callback_query.data)
    query_id = action.payload.prepared_collection_id
    books = LibraryController.find_books_by_query_id(query_id)

    message = callback_query.message

    message_creator = MessageFabric.create_page_message(books, action=action)

    await message_creator.edit_to(message)


@dp.message_handler(content_types=ContentType.ANY)
async def unknown_type_of_message(msg: types.Message):
    await bot.send_sticker(
        chat_id=msg.from_user.id,
        sticker=r"CAACAgIAAxkBAAEG6K9jocRBRnn3HykoJBwDzHVxv3FN5wACEgADbrttNcV0uCSF9fevLAQ"
    )


def start():
    executor.start_polling(dp)
    BookController.finalize()
    QueryController.finalize()
    CategoryController.finalize()
    UserController.finalize()
