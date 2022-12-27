from telegram_bot.controllers.keyboard_controller import KeyboardController
from telegram_bot.controllers.message_creator import MessageCreator


class Messages:
    start_message = MessageCreator(

        """
Радий Вас бачити,  {name}! 🎓
Я бот написано на Python 🐍 для пошуку книг у бібліотеці ДУТ (Державний університет телекомунікацій) по:  

💻 Інформаційних технологій
🔐 Захисту інформації
📡 Телекомунікацій
🗃 Менеджменту та підприємництва

Зараз у боті: 📚
Кількість користувачів: 
    
Ми надаємо вам можливість вибрати за яким параметром ви хочете шукати. Давайте почнемо?""".format(name="fd"),
        reply_markup=KeyboardController.create_start_keyboard()
    )


    no_book_message = MessageCreator(
        "Такої книги немає чи запит не вірний!",
        reply_markup=KeyboardController.create_back_to_main_menu_keyboard()
    )

    global_category_pick_message = MessageCreator(
        "1",
        reply_markup=KeyboardController.create_global_categories_keyboard()
    )
