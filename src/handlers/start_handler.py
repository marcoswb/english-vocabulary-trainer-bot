from telegram import Update
from telegram.ext import ContextTypes
from src.handlers.base_handler import BaseHandler


class Start(BaseHandler):

    @classmethod
    async def init(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await cls.send_message(update, context, "I'm a bot, please talk to me!")
