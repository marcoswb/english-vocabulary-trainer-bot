from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes


class BaseHandler:

    @classmethod
    def get_message(cls, update: Update):
        return ' '.join(update.message.text.split(' ')[1:])

    @classmethod
    async def send_message(cls, update: Update, context: ContextTypes.DEFAULT_TYPE, message: str):
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode="HTML")

    @classmethod
    async def question_message(cls, update: Update, context: ContextTypes.DEFAULT_TYPE, message: str, callback_func):
        context.user_data['callback_function'] = callback_func
        await update.message.reply_text(message)

    @classmethod
    def storage_info(cls, context: ContextTypes.DEFAULT_TYPE, key: str, value):
        context.user_data[key] = value

    @classmethod
    def get_info_storage(cls, context: ContextTypes.DEFAULT_TYPE, key: str):
        return context.user_data.get(key)

    @classmethod
    async def ask_confirm(cls, update: Update, context: ContextTypes.DEFAULT_TYPE, message: str, callback_func):
        context.user_data['callback_function'] = callback_func
        keyboard = [
            [InlineKeyboardButton('Sim', callback_data='yes')],
            [InlineKeyboardButton('Não', callback_data='no')],
        ]
        await update.message.reply_text(
            message,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML"
        )

    @classmethod
    async def finish(cls, update: Update, context: ContextTypes.DEFAULT_TYPE, message: str):
        context.user_data.clear()
        await cls.send_message(update, context, message)
