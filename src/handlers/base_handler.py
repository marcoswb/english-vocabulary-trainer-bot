from telegram import Update
from telegram.ext import ContextTypes


class BaseHandler:

    @classmethod
    def get_message(cls, update: Update):
        return ' '.join(update.message.text.split(' ')[1:])

    @classmethod
    async def send_message(cls, update: Update, context: ContextTypes.DEFAULT_TYPE, message: str):
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode="HTML")