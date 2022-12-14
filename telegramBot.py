from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import TOKEN
from database import DatabaseConnect
from models import Book

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nНапиши мне название книги!\nЗапрос должен содержать минимум 3 символа!")


@dp.message_handler()
async def echo_message(msg: types.Message):

    if len(msg.text) < 3:
        await bot.send_message(msg.from_user.id, "Запрос должен содержать минимум 3 символа!")
        return

    book_list = DatabaseConnect.find_by_title(msg.text)

    for book in book_list:
        await bot.send_message(msg.from_user.id,
                "Название книги: " + str(book.title) + "\n"
                "Id в бд " + str(book.id) + "\n"                          
                "Автор: " + str(book.author) + "\n"
                "Год публикации " + str(book.year_of_publication) + "\n"
                "Ссылка " + str(book.link) + "\n")

if __name__ == '__main__':
    executor.start_polling(dp)
    DatabaseConnect.finalize()
