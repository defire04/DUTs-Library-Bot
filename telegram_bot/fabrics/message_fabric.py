from typing import List
from controllers.message_controller import MessageController

from models.book import Book
from models.search_result import PagesResult, SearchResult
from telegram_bot.actions.action_creator import ButtonAction, ButtonPageActionPayload
from telegram_bot.controllers.keyboard_controller import KeyboardController
from telegram_bot.controllers.message_creator import MessageCreator
from util.xor import XOR


class MessageFabric:
    @staticmethod
    def create_page_message(books: List[Book], action: ButtonAction[ButtonPageActionPayload] | None = None, query_id: int | None = None) -> MessageCreator:

        if not XOR(action, query_id):
            raise TypeError("query_id or action must be specified")
        
        page_index = 0
        sort_direction = 0

        if action:

            page_index = action.payload.page_index
            query_id = action.payload.prepared_collection_id
            sort_direction = action.payload.sort_direction


        search_result = SearchResult(books, query_id)
        pages = PagesResult(search_result)

        keyboard = KeyboardController.create_pages_keyboard(pages, page_index, sort_direction)

        message_text = MessageController.prepare_page_message(pages.get_page(page_index))

        return MessageCreator(message_text, keyboard)
        