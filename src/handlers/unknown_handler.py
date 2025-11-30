from telegram import Update
from telegram.ext import ContextTypes
from src.handlers.base_handler import BaseHandler


class Unknown(BaseHandler):

    @classmethod
    async def init(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await cls.send_message(update, context, "Sorry, I didn't understand that command.")
