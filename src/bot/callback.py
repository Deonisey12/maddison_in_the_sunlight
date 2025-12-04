import sys
sys.path.append("src/bot")

from entities.database import Database
import telegram as tg
import telegram.ext as tgx

from cmd_dictionary import UserData, Actions
from callbacks import CreateCallback, FormCallback, ListCallback


class CallbackHandler:
    def __init__(self, database: Database):
        self._database = database
        self._create_callback = CreateCallback()
        self._form_callback = FormCallback(database)
        self._list_callback = ListCallback(database)

    async def execute(self, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()

        callback_data = query.data
        
        if not callback_data or not context:
            return
        
        if ":" in callback_data:
            action, data = callback_data.split(":", 1)
        else:
            return

        if action == Actions.CREATE:
            await self._create_callback.execute(update, context, data)
        elif action == Actions.TEST_FORM:
            await self._form_callback.execute(update, context, data)
        elif action == Actions.LIST:
            await self._list_callback.execute(update, context, data)
        else:
            await query.edit_message_text(text=f"Неизвестное действие: {action}")

