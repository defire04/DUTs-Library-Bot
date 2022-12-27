from aiogram import types

from models.messages import Messages


async def process_help_info_command(msg: types.Message):
    # UserController.add_new_user(msg) maybe add update user time

    await msg.answer(**Messages.help_info_message.get_args())
    await msg.delete()
