import asyncio
from telegram import Bot
from telegram.error import Forbidden
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler
)
import src.utils.functions as func
from src.handlers.start_handler import Start
from src.handlers.add_word_handler import AddWord
from src.handlers.message_response_handler import MessageResponseHandler
from src.handlers.unknown_handler import Unknown

async def warn_user():
    try:
        bot = Bot(token=func.get_env('TOKEN_BOT'))
        await bot.send_message(
            chat_id=func.get_env('AUTHORIZED_USER_ID'),
            text='Olá! Seu quiz diário está pronto.\nDigite /start para começar ▶️'
        )
    except Forbidden:
        print(f"Usuário {func.get_env('AUTHORIZED_USER_ID')} bloqueou o bot.")

def start_quiz():
    application = ApplicationBuilder().token(func.get_env('TOKEN_BOT')).build()

    application.add_handler(CommandHandler('start', Start.init))
    application.add_handler(CommandHandler('add', AddWord.init))
    application.add_handler(MessageHandler(filters.TEXT, MessageResponseHandler.response_str))
    application.add_handler(CallbackQueryHandler(MessageResponseHandler.response_query))
    application.add_handler(MessageHandler(filters.COMMAND, Unknown.init))

    application.run_polling()


if __name__ == '__main__':
    asyncio.run(warn_user())
    start_quiz()