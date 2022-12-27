from aiogram import types
from models.sorting_field import SortingFieldsEnum

from telegram_bot.actions.action_creator import ButtonAction, ButtonPageActionPayload
from telegram_bot.controllers.library_controller import LibraryController
from telegram_bot.fabrics.message_fabric import MessageFabric


fields_count = 3

async def sort_field_change_handler(callback_query: types.CallbackQuery):
    message = callback_query.message
    action = ButtonAction[ButtonPageActionPayload].from_json(callback_query.data)
    query_id = action.payload.prepared_collection_id
    books = LibraryController.find_books_by_query_id(query_id)
    field_index = action.payload.sort_field

    field_index += 1
    field_index = 0 if field_index >= fields_count or field_index < 0 else field_index
    action.payload.sort_field = field_index
    if not action.payload.sort_direction:
        action.payload.sort_direction = 1

    message = callback_query.message

    message_creator = MessageFabric.create_page_message(books, action=action)

    await message_creator.edit_to(message)