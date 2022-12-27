from aiogram import types

from controllers.book_controller import BookController
from controllers.user_controller import UserController

from models.messages import Messages


async def process_start_command(msg: types.Message):
    UserController.add_new_user(msg)

    await msg.answer(**Messages.start_message.format(
        name=msg.from_user.full_name,
        book_in_db=str(BookController.count_of_books()),
        count_of_users=str(len(UserController.get_users()))
    ).get_args())
    await msg.delete()
