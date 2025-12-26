from telegram import Update
from telegram.ext import ContextTypes
from src.handlers.base_handler import BaseHandler
from src.utils.decorator_auth import only_authorized


class Unknown(BaseHandler):

    @classmethod
    @only_authorized
    async def init(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await cls.send_message(update, context, "Sorry, I didn't understand that command.")
