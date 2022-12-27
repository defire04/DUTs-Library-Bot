from aiogram import types

from models.messages import Messages


async def process_main_menu_command(msg: types.Message):
    # UserController.add_new_user(msg) maybe add update user time

    await msg.answer(**Messages.main_menu_message.get_args())
    await msg.delete()
