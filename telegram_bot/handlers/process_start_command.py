from aiogram import types
from controllers.user_controller import UserController

from models.messages import Messages
from resources.config import admins

ADMINS = admins


async def process_start_command(msg: types.Message):
    UserController.add_new_user(msg)
    if msg.from_user.id in ADMINS:
        await msg.answer('Добро пожаловать в Админ-Панель! Выберите действие на клавиатуре')
    else:
        await msg.answer(**Messages.start_message.get_args())

    await msg.delete()
