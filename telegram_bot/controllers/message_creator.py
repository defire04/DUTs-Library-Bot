from typing import Dict

from aiogram.types import InlineKeyboardMarkup, Message, ParseMode
from collections import namedtuple

MessageArgs = namedtuple('MessageArgs', 'text parse_mode reply_markup')


class MessageCreator:
    def __init__(self, content: str, reply_markup: InlineKeyboardMarkup | None = None,
                 parse_mode: str | None = ParseMode.HTML) -> None:
        self.content = content
        self.reply_markup = reply_markup
        self.parse_mode = parse_mode

    def get_args(self) -> dict[str, bool | str | InlineKeyboardMarkup | None]:
        return {
            'text': self.content,
            'parse_mode': self.parse_mode,
            'reply_markup': self.reply_markup,
        }

    def format(self, **kwargs):
        return MessageCreator(self.content.format(**kwargs), self.reply_markup, self.parse_mode)

    async def edit_to(self, message: Message) -> None:
        await message.edit_text(self.content, parse_mode=self.parse_mode)
        await message.edit_reply_markup(self.reply_markup)
