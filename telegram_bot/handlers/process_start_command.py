from aiogram import types
from controllers.user_controller import UserController

from models.messages import Messages
from resources.config import admins

ADMINS = admins


async def process_start_command(msg: types.Message):
    if msg.from_user.id in ADMINS:
        UserController.add_new_admin(msg)
    else:
        UserController.add_new_user(msg)

    await msg.answer(**Messages.start_message.get_args())
    await msg.delete()
