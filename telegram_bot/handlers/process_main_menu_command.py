from aiogram import types

from controllers.book_controller import BookController
from controllers.user_controller import UserController

from models.messages import Messages
from resources.config import admins

ADMINS = admins


async def process_main_menu_command(msg: types.Message):
    UserController.add_new_user(msg)

    await msg.answer(**Messages.main_menu_message.get_args())
    await msg.delete()