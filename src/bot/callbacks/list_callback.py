import sys
sys.path.append("src/bot")

import telegram as tg
import telegram.ext as tgx


async def handle_list_callback(update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE, data: str):
    query = update.callback_query
    pass

