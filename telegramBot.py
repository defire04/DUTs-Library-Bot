from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import TOKEN
from database import DatabaseConnect

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nНапиши мне название книги!")


@dp.message_handler()
async def echo_message(msg: types.Message):
    book_list = DatabaseConnect.find_by_title(msg.text)

    for book in book_list:
        await bot.send_message(msg.from_user.id, book)


if __name__ == '__main__':
    executor.start_polling(dp)
