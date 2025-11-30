from telegram import Update
from telegram.ext import ContextTypes
from src.handlers.base_handler import BaseHandler

class AddWord(BaseHandler):

    @classmethod
    async def init(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
        new_word = cls.get_message(update).upper()
        await cls.send_message(update, context, f"Adicionando <strong>{new_word}</strong> ao vocabulário.")
