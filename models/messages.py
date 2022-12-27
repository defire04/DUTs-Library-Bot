from telegram_bot.controllers.keyboard_controller import KeyboardController
from telegram_bot.controllers.message_creator import MessageCreator

class Messages:
    start_message = MessageCreator(
        "Добро пожаловать в DUT Library!\nВыберите в меню как вы хотите искать\n",
        reply_markup=KeyboardController.create_main_menu_keyboard()
    )

    no_book_message = MessageCreator(
        "Такой книги нет или запрос не верен!",
        reply_markup=KeyboardController.create_back_to_main_menu_keyboard()
    )

    global_category_pick_message = MessageCreator(
        "1",
        reply_markup=KeyboardController.create_global_categories_keyboard()
    )
