from aiogram import types
from actions.action_creator import ButtonAction, ButtonCategoryActionPayload
from controllers.keyboard_controller import KeyboardController
from controllers.message_creator import MessageCreator
from models.actions import Actions
from models.messages import Messages

from util.filter_query_by_action import create_filter_query_by_action

async def open_category_search_handler(callback_query: types.CallbackQuery):
    message = callback_query.message
    await Messages.global_category_pick_message.edit_to(message)

async def global_category_search_handler(callback_query: types.CallbackQuery):
    message = callback_query.message
    action = ButtonAction[ButtonCategoryActionPayload].from_json(callback_query.data)
    id = action.payload.categry_id
    message_creator = MessageCreator(
        "2",
        reply_markup=KeyboardController.create_sub_categories_keyboard(id)
    )
    await message_creator.edit_to(message)

async def sub_category_search_handler(callback_query: types.CallbackQuery):
    message = callback_query.message
    action = ButtonAction[ButtonCategoryActionPayload].from_json(callback_query.data)
    id = action.payload.categry_id
    print('3')
    message_creator = MessageCreator(
        "3",
        reply_markup=KeyboardController.create_book_categories_keyboard(id)
    )
    await message_creator.edit_to(message)


async def book_category_search_handler(callback_query: types.CallbackQuery):
    message = callback_query.message
    message_creator = MessageCreator(
        "Books check"
    )
    await message_creator.edit_to(message)


def create_filter_category_action_by_type(category_type: int):
    def filter(action: ButtonAction[ButtonCategoryActionPayload]):
        return action.payload.category_type == category_type
    return create_filter_query_by_action(Actions.TO_CATEGORY_MENU, filter)