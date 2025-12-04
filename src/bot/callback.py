import sys
sys.path.append("src/bot")

from entities.database import Database
import telegram as tg
import telegram.ext as tgx

from cmd_dictionary import UserData, Actions
from callbacks import handle_create_callback, handle_form_callback, handle_list_callback


class CallbackHandler:
    def __init__(self, database: Database):
        self._database = database

    async def execute(self, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()

        message_id = query.message.message_id
        form_actions = context.user_data.get(UserData.FORM_ACTIONS, {})
        action = form_actions.get(message_id, Actions.CREATE)
        callback_data = query.data

        if action == Actions.CREATE:
            await handle_create_callback(update, context, callback_data)
        elif action == Actions.TEST_FORM:
            await handle_form_callback(self._database, update, context, callback_data)
        elif action == Actions.LIST:
            await handle_list_callback(update, context, callback_data)
        else:
            await query.edit_message_text(text=f"Неизвестное действие: {action}")

