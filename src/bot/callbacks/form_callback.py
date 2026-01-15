import sys
sys.path.append("src/bot")

from entities.database import Database
import telegram as tg
import telegram.ext as tgx

from forms.base_form import BaseForm
from users.userdata import UserData
from .base_callback import BaseCallback
from cmd_dictionary import (
    MARKDOWN_V2,
    Actions,
    FormState,
    UserState,
    )

class FormCallback(BaseCallback):
    def __init__(self, database: Database):
        self._database = database

    async def execute(self, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE, data: str):
        query = update.callback_query
        state = context.user_data.get(UserState.FORM_STATE, {})

        if not state or not state.get(FormState.ACTIVE):
            return

        user_state = UserData.LoadByName(state[FormState.USER_NAME])
        
        entity_id = int(data)
        entity = self._database.GetEntityById("Event", entity_id)
        
        if entity:
            entity_info = f"*{str(entity.name)}*\n\n{str(entity.disc)}"
        else:
            entity_info = "Сущность не найдена"

        entity.Use(user_state)

        await query.edit_message_text(text=entity_info, parse_mode=MARKDOWN_V2)
        
