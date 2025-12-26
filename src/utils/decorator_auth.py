from functools import wraps
from src.utils.functions import get_env

AUTHORIZED_USER_ID = int(get_env('AUTHORIZED_USER_ID'))

def only_authorized(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        if len(args) == 2:
            update, context = args
        else:
            _, update, context = args[:3]

        user = update.effective_user
        chat = update.effective_chat

        if (
            not user
            or user.id != AUTHORIZED_USER_ID
            or chat.type != 'private'
        ):
            if update.callback_query:
                await update.callback_query.answer(
                    'Acesso negado.',
                    show_alert=True
                )
            return

        return await func(*args, **kwargs)

    return wrapper
