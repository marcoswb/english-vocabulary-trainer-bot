from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters
)
import src.utils as func
from src.start_handler import start_handler
from src.unknown_handler import unknown_handler


if __name__ == '__main__':
    application = ApplicationBuilder().token(func.get_env('TOKEN_BOT')).build()

    application.add_handler(CommandHandler('start', start_handler))
    application.add_handler(MessageHandler(filters.COMMAND, unknown_handler))

    application.run_polling()