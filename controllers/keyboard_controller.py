from typing import List
from actions.action_creator import ButtonCategoryAction, ButtonMenuAction, ButtonPageAction
from controllers.category_controller import CategoryController
from models.actions import Actions
from models.category import CategoriesEnum, Category
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
        search_action = ButtonMenuAction(Actions.START_SEARCH)
        search_button = InlineKeyboardButton('Search book', callback_data=search_action.stringify())
        category_action = ButtonMenuAction(Actions.OPEN_CATEGORY_SEARCH)
        category_button = InlineKeyboardButton('Categories', callback_data=category_action.stringify())
        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(search_button)
        keyboard.add(category_button)
        return keyboard

    @staticmethod
    def create_back_to_main_menu_keyboard():
        keyboard = InlineKeyboardMarkup()
        keyboard.add(KeyboardController.create_to_main_menu_button())
        return keyboard

    @staticmethod
    def create_global_categories_keyboard():
        return KeyboardController.create_categories_keyboard(CategoryController.get_global_categories(), CategoriesEnum.GLOBAL)
        
    @staticmethod
    def create_sub_categories_keyboard(global_id: int):
        return KeyboardController.create_categories_keyboard(CategoryController.find_sub_categories_by_global_id(global_id), CategoriesEnum.SUB)

    @staticmethod
    def create_book_categories_keyboard(sub_id: int):
        return KeyboardController.create_categories_keyboard(CategoryController.find_book_categories_by_sub_id(sub_id), CategoriesEnum.BOOK)

    @staticmethod
    def create_categories_keyboard(category_list: List[Category], category_type: int):
        keyboard = InlineKeyboardMarkup()
        for category in category_list:
            action = ButtonCategoryAction(category.id, category_type)
            button = InlineKeyboardButton(category.title, callback_data=action.stringify())
            keyboard.insert(button)
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
