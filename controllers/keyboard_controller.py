from actions.action_creator import ButtonPageAction
from models.search_result import PagesResult
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class KeyboardController:
    @staticmethod
    def create_pages_keyboard(pages: PagesResult, page_index: int):
        query_id = pages.result.search_query_id

        keyboard = InlineKeyboardMarkup(row_width=2)
        if page_index > 0:
            keyboard.insert(KeyboardController.create_previous_button(page_index, query_id))
        if pages.get_total_pages_count() - 1 > page_index:
            keyboard.insert(KeyboardController.create_next_button(page_index, query_id))

        return keyboard

    @staticmethod
    def create_previous_button(current_page_index: int, query_id: int):
        return KeyboardController.create_page_button("Back", current_page_index - 1, query_id)

    @staticmethod
    def create_next_button(current_page_index: int, query_id: int):
        return KeyboardController.create_page_button("Next", current_page_index + 1, query_id)

    @staticmethod
    def create_page_button(text: str, page_index: int, query_id: int):
        action = ButtonPageAction(page_index, query_id)
        button = InlineKeyboardButton(text, callback_data=action.stringify())
        return button
