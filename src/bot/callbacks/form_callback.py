import sys
sys.path.append("src/bot")

from entities.database import Database
import telegram as tg
import telegram.ext as tgx

from base_form import BaseForm
from cmd_dictionary import MARKDOWN_V2


async def handle_form_callback(database: Database, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE, data: str):
    query = update.callback_query
    
    entity_id = int(data)
    entity = database.GetEntityById("Event", entity_id)
    
    if entity:
        escaped_name = BaseForm.escape_markdown_v2(str(entity.name))
        escaped_disc = BaseForm.escape_markdown_v2(str(entity.disc))
        entity_info = f"*{escaped_name}*\n\n{escaped_disc}"
        await query.edit_message_text(text=entity_info, parse_mode=MARKDOWN_V2)
    else:
        await query.edit_message_text(text="Сущность не найдена")

