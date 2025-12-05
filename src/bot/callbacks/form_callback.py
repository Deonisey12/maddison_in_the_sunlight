import sys
sys.path.append("src/bot")

from entities.database import Database
import telegram as tg
import telegram.ext as tgx

from forms.base_form import BaseForm
from cmd_dictionary import MARKDOWN_V2
from .base_callback import BaseCallback


class FormCallback(BaseCallback):
    def __init__(self, database: Database):
        self._database = database

    async def execute(self, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE, data: str):
        query = update.callback_query
        
        entity_id = int(data)
        entity = self._database.GetEntityById("Event", entity_id)
        
        if entity:
            entity_info = f"*{str(entity.name)}*\n\n{str(entity.disc)}"
            await query.edit_message_text(text=entity_info, parse_mode=MARKDOWN_V2)
        else:
            await query.edit_message_text(text="Сущность не найдена")

