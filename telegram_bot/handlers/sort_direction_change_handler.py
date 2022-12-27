from aiogram import types

from telegram_bot.actions.action_creator import ButtonAction, ButtonPageActionPayload
from telegram_bot.controllers.library_controller import LibraryController
from telegram_bot.fabrics.message_fabric import MessageFabric


direction_next_values_by_current_value = {
    1: -1,
    0: 1,
    -1: 0
}

async def sort_direction_change_handler(callback_query: types.CallbackQuery):
    message = callback_query.message
    action = ButtonAction[ButtonPageActionPayload].from_json(callback_query.data)
    query_id = action.payload.prepared_collection_id
    books = LibraryController.find_books_by_query_id(query_id)
    direction = action.payload.sort_direction

    direction = direction_next_values_by_current_value[direction]
    
    action.payload.sort_direction = direction

    message = callback_query.message

    message_creator = MessageFabric.create_page_message(books, action=action)

    await message_creator.edit_to(message)