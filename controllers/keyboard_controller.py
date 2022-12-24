from actions.action_creator import ButtonMenuAction, ButtonPageAction
from models.actions import Actions
from models.search_result import PagesResult
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, ReplyKeyboardRemove


class KeyboardController:
    @staticmethod
    def create_pages_keyboard(pages: PagesResult, page_index: int):
        query_id = pages.result.search_query_id

        keyboard = InlineKeyboardMarkup(row_width=2)
        if page_index > 0:
            keyboard.insert(KeyboardController.create_previous_button(page_index, query_id))
        if pages.get_total_pages_count() - 1 > page_index:
            keyboard.insert(KeyboardController.create_next_button(page_index, query_id))
        
        keyboard.add(KeyboardController.create_to_main_menu_button())

        return keyboard

    @staticmethod
    def create_start_keyboard():
        action = ButtonMenuAction(Actions.START_SEARCH)
        keyboard = InlineKeyboardMarkup(row_width=2)
        search_button = InlineKeyboardButton('Search book', callback_data=action.stringify())
        keyboard.add(search_button)
        return keyboard

    @staticmethod
    def create_back_to_main_menu_keyboard():
        keyboard = InlineKeyboardMarkup()
        keyboard.add(KeyboardController.create_to_main_menu_button())
        return keyboard

    

    @staticmethod
    def create_previous_button(current_page_index: int, query_id: int):
        return KeyboardController.create_page_button("◀ Back", current_page_index - 1, query_id)

    @staticmethod
    def create_next_button(current_page_index: int, query_id: int):
        return KeyboardController.create_page_button("Next ▶", current_page_index + 1, query_id)

    @staticmethod
    def create_page_button(text: str, page_index: int, query_id: int):
        action = ButtonPageAction(page_index, query_id)
        button = InlineKeyboardButton(text, callback_data=action.stringify())
        return button

    @staticmethod
    def create_to_main_menu_button():
        action = ButtonMenuAction(Actions.TO_MAIN_MENU)
        button = InlineKeyboardButton('Back to main menu', callback_data=action.stringify())
        return button

    @staticmethod
    async def remove_inline_keyboard(msg: Message):
        msg = await msg.answer('loading...', reply_markup=ReplyKeyboardRemove())
        await msg.delete()
