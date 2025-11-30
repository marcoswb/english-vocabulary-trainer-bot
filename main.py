from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters
)
import src.utils.functions as func
from src.handlers.start_handler import Start
from src.handlers.add_word_handler import AddWord
from src.handlers.unknown_handler import Unknown


if __name__ == '__main__':
    application = ApplicationBuilder().token(func.get_env('TOKEN_BOT')).build()

    application.add_handler(CommandHandler('start', Start.init))
    application.add_handler(CommandHandler('add', AddWord.init))
    application.add_handler(MessageHandler(filters.COMMAND, Unknown.init))

    application.run_polling()