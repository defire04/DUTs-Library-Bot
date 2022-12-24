from controllers.keyboard_controller import KeyboardController
from controllers.message_creator import MessageCreator

class Messages:
    start_message = MessageCreator(
        "Добро пожаловать в DUT Library!\nВыберите в меню как вы хотите искать\n",
        reply_markup=KeyboardController.create_start_keyboard()
    )

    no_book_message = MessageCreator(
        "Такой книги нет или запрос не верен!",
        reply_markup=KeyboardController.create_back_to_main_menu_keyboard()
    )

