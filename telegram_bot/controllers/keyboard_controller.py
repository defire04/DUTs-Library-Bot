from typing import List
from models.sorting_field import SortingFieldsEnum
from telegram_bot.actions.action_creator import ButtonCategoryAction, ButtonMenuAction, ButtonPageChangeAction, \
    ButtonPageSortDirectionAction, ButtonPageSortFieldAction
from controllers.category_controller import CategoryController
from models.actions import Actions
from models.category import CategoriesEnum, Category
from models.search_result import PagesResult
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, ReplyKeyboardRemove


class KeyboardController:
    @staticmethod
    def create_pages_keyboard(pages: PagesResult, page_index: int = 0, sort_direction: int = 0, sort_object: int = 0):
        query_id = pages.result.search_query_id

        keyboard = InlineKeyboardMarkup(row_width=3)
        if page_index > 0:
            keyboard.insert(KeyboardController.create_previous_button(page_index, query_id, sort_direction, sort_object))
        if pages.get_total_pages_count() - 1 > page_index:
            keyboard.insert(KeyboardController.create_next_button(page_index, query_id, sort_direction, sort_object))

        keyboard.add(KeyboardController.create_sort_filed_button(query_id, sort_direction, sort_object))
        keyboard.insert(KeyboardController.create_sort_direction_button(query_id, sort_direction, sort_object))
        keyboard.insert(KeyboardController.create_to_main_menu_button())

        return keyboard

    @staticmethod
    def create_main_menu_keyboard():
        search_action = ButtonMenuAction(Actions.START_SEARCH)
        search_button = InlineKeyboardButton('📘 Назва книги', callback_data=search_action.stringify())
        category_action = ButtonMenuAction(Actions.OPEN_CATEGORY_SEARCH)
        category_button = InlineKeyboardButton('📜 Категорії', callback_data=category_action.stringify())
        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(search_button)
        keyboard.add(category_button)
        return keyboard

    @staticmethod
    def create_start_menu_keyboard():
        keyboard = InlineKeyboardMarkup()
        keyboard.add(KeyboardController.create_to_main_menu_button("Розпочати!"))
        return keyboard

    @staticmethod
    def create_back_to_main_menu_keyboard():
        keyboard = InlineKeyboardMarkup()
        keyboard.add(KeyboardController.create_to_main_menu_button())
        return keyboard

    @staticmethod
    def create_global_categories_keyboard():
        keyboard = KeyboardController.create_categories_keyboard(CategoryController.get_global_categories(),
                                                             CategoriesEnum.GLOBAL)
        keyboard.add(KeyboardController.create_to_main_menu_button())
        return keyboard

    @staticmethod
    def create_sub_categories_keyboard(global_id: int):
        keyboard = KeyboardController.create_categories_keyboard(
            CategoryController.find_sub_categories_by_global_id(global_id), CategoriesEnum.SUB)
        # keyboard.add(KeyboardController.create_open_category_search_button('Назад ◀'))
        keyboard.add(KeyboardController.create_to_main_menu_button())
        return keyboard

    @staticmethod
    def create_book_categories_keyboard(sub_id: int):
        keyboard = KeyboardController.create_categories_keyboard(CategoryController.find_book_categories_by_sub_id(sub_id),
                                                             CategoriesEnum.BOOK)
        # keyboard.add(KeyboardController.create_category_button('Назад ◀', CategoriesEnum.SUB, sub))
        keyboard.add(KeyboardController.create_to_main_menu_button())

        return keyboard

    @staticmethod
    def create_categories_keyboard(category_list: List[Category], category_type: int):
        keyboard = InlineKeyboardMarkup()
        for category in category_list:
            keyboard.add(KeyboardController.create_category_button(
                title=category.title,
                category_type=category_type,
                category_id=category.id
            ))

        return keyboard
    
    @staticmethod
    def create_category_button(title: str, category_type: int, category_id: str):
        action = ButtonCategoryAction(category_id, category_type)
        button = InlineKeyboardButton(title, callback_data=action.stringify())
        return button

    @staticmethod
    def create_open_category_search_button(text: str):
        category_action = ButtonMenuAction(Actions.OPEN_CATEGORY_SEARCH)
        category_button = InlineKeyboardButton(text, callback_data=category_action.stringify())
        return category_button

    @staticmethod
    def create_previous_button(current_page_index: int, query_id: int, sort_direction: int = 0, sort_object: int = 0):
        return KeyboardController.create_page_change_button("◀ Попередня", current_page_index - 1, query_id, sort_direction, sort_object)

    @staticmethod
    def create_next_button(current_page_index: int, query_id: int, sort_direction: int = 0, sort_object: int = 0):
        return KeyboardController.create_page_change_button("Наступна ▶", current_page_index + 1, query_id, sort_direction, sort_object)

    @staticmethod
    def create_page_change_button(text: str, page_index: int, query_id: int, sort_direction: int, sort_object: int):
        action = ButtonPageChangeAction(page_index, query_id, sort_direction, sort_object)
        button = InlineKeyboardButton(text, callback_data=action.stringify())
        return button

    @staticmethod
    def create_page_sort_direction_button(text: str, page_index: int, query_id: int, sort_direction: int, sort_object: int):
        action = ButtonPageSortDirectionAction(page_index, query_id, sort_direction, sort_object)
        button = InlineKeyboardButton(text, callback_data=action.stringify())
        return button
    
    @staticmethod
    def create_page_sort_object_button(text: str, page_index: int, query_id: int, sort_direction: int, sort_object: int):
        action = ButtonPageSortFieldAction(page_index, query_id, sort_direction, sort_object)
        button = InlineKeyboardButton(text, callback_data=action.stringify())
        return button

    @staticmethod
    def create_to_main_menu_button(text: str | None = None):
        button_text = text if text else 'Меню ↩'
        action = ButtonMenuAction(Actions.TO_MAIN_MENU)
        button = InlineKeyboardButton(button_text, callback_data=action.stringify())
        return button


    @staticmethod
    def create_sort_direction_button(query_id: int, sort_direction: int = 0, sort_object: int = 0):
        button_text = ""
        if sort_direction == 0:
            button_text += "↕"
        if sort_direction == -1:
            button_text += "⏬"
        if sort_direction == 1:
            button_text += "⏫"
        button = KeyboardController.create_page_sort_direction_button(button_text, 0, query_id, sort_direction, sort_object)
        return button

    @staticmethod
    def create_sort_filed_button(query_id: int, sort_direction: int = 0, sort_object: int = 0):
        button_text = "Сорт. за "
        sorting_texts = {
            SortingFieldsEnum.AUTHOR: '👴',
            SortingFieldsEnum.TITLE: '📚',
            SortingFieldsEnum.YEAR: '📆'
        }
        sorting_text = sorting_texts[sort_object]

        if sorting_text: button_text += sorting_text
        button = KeyboardController.create_page_sort_object_button(button_text, 0, query_id, sort_direction, sort_object)
        return button

    @staticmethod
    async def remove_inline_keyboard(msg: Message):
        msg = await msg.answer('завантаження...', reply_markup=ReplyKeyboardRemove())
        await msg.delete()
