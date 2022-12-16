from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from controllers.parser import Parser
from resources.config import TOKEN
from services.book_service import BookService
from actions.action_creator import ButtonAction, ButtonPageAction, Actions
from util.util import string_trim

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

action = ButtonPageAction(1, 2)
button = InlineKeyboardButton('Text', callback_data=action.stringify())
inline_kb_full = InlineKeyboardMarkup(row_width=2).add(button)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nНапиши мне название книги!\nЗапрос должен содержать минимум 3 символа!",
                        reply_markup=inline_kb_full)


@dp.message_handler()
async def echo_message(msg: types.Message):
    if len(msg.text) < 2:
        await bot.send_message(msg.from_user.id, "Запрос должен содержать минимум 2 символа!")
        return

    book_list = BookService.find_by_title(msg.text)

    if not book_list:
        await bot.send_message(msg.from_user.id, "Такой книги нет или запрос не верен!")
        return

    for book in book_list:
        await bot.send_message(msg.from_user.id,
                               "Название книги: " +
                                string_trim(str(book.title)) + "\n"
                                "Id в бд: " + str(book.id) + "\n"
                                "Автор: " + string_trim( str(book.author)) + "\n"
                                "Год публикации: " + str(book.year_of_publication) + "\n"
                                "Ссылка: " + str(book.link) + "\n")


@dp.callback_query_handler(lambda callback: callback.data and ButtonAction.from_json(callback.data)
                           .id == Actions.SWITCH_PAGE)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    action = ButtonAction.from_json(callback_query.data)
    print(action.payload.page_index)
    print(action.payload.prepared_collection_id)

    await bot.answer_callback_query(callback_query.id, text='Нажата вторая кнопка')


if __name__ == '__main__':
    executor.start_polling(dp)
    BookService.finalize()
