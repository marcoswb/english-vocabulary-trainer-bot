import sys
from telegram import Update
from telegram.ext import ContextTypes
from src.handlers.base_handler import BaseHandler

class MessageResponseHandler(BaseHandler):

    @classmethod
    async def response_str(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            response = update.message.text

            callback = context.user_data.get('callback_function')
            if callback:
                await callback(update, context, response)
        except Exception as error:
            await cls.send_error(update, context, error, sys.exc_info())

    @classmethod
    async def response_query(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            query = update.callback_query
            await query.answer()

            callback = context.user_data.get('callback_function')
            if callback:
                await callback(update, context, query.data)
        except Exception as error:
            await cls.send_error(update, context, error, sys.exc_info())
