from aiogram import types
from telegram_bot.actions.action_creator import ButtonAction, ButtonCategoryActionPayload
from telegram_bot.controllers.keyboard_controller import KeyboardController
from telegram_bot.controllers.message_creator import MessageCreator
from models.actions import Actions
from models.messages import Messages
from controllers.book_controller import BookController
from operator import itemgetter
from telegram_bot.fabrics.message_fabric import MessageFabric

from util.filter_query_by_action import create_filter_query_by_action


async def open_category_search_handler(callback_query: types.CallbackQuery):
    message = callback_query.message

    await Messages.global_category_pick_message.edit_to(message)


async def global_category_search_handler(callback_query: types.CallbackQuery):
    message = callback_query.message
    action = ButtonAction[ButtonCategoryActionPayload].from_json(callback_query.data)
    id = action.payload.categry_id
    message_creator = MessageCreator(
        "👇 Тепер оберіть підкатегорію з нижче наведених 👇",
        reply_markup=KeyboardController.create_sub_categories_keyboard(id)
    )
    await message_creator.edit_to(message)


async def sub_category_search_handler(callback_query: types.CallbackQuery):
    message = callback_query.message
    action = ButtonAction[ButtonCategoryActionPayload].from_json(callback_query.data)
    id = action.payload.categry_id
    message_creator = MessageCreator(
        "👇 Оберіть категорію з якої б ви хотіли почитати книги 👇",
        reply_markup=KeyboardController.create_book_categories_keyboard(id)
    )
    await message_creator.edit_to(message)


async def book_category_search_handler(callback_query: types.CallbackQuery):
    message = callback_query.message
    action = ButtonAction[ButtonCategoryActionPayload].from_json(callback_query.data)

    books, query_id = itemgetter('books', 'query_id')(
        BookController.find_by_book_category_and_create_query(action.payload.categry_id))

    message_creator = MessageFabric.create_page_message(books, query_id=query_id)

    await message_creator.edit_to(message)


def create_filter_category_action_by_type(category_type: int):
    def filter(action: ButtonAction[ButtonCategoryActionPayload]):
        return action.payload.category_type == category_type

    return create_filter_query_by_action(Actions.TO_CATEGORY_MENU, filter)
