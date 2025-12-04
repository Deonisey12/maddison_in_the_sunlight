import sys
sys.path.append("src/bot")

import telegram as tg
import telegram.ext as tgx

from entities.database import Database
from generators.generator import Generator
from generators.list import Entities

from .base_callback import BaseCallback
from bot.cmd_dictionary import MARKDOWN_V2


class ListCallback(BaseCallback):
    def __init__(self, database: Database):
        self._database = database
        self._generator = Generator()

    async def execute(self, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE, data: str):
        query = update.callback_query
        
        type_key = list(Entities.keys())[int(data)]
        entity_ids = sorted(self._database._db.get(type_key, {}).items())

        list = []
        for e in entity_ids:
            entity = self._database.GetEntityById(type_key, e[0])
            if entity:
                entity_obj = self._generator.Load(type_key, entity.filename)
                list.append(entity_obj)

        # await query.edit_message_text(text=str(list), parse_mode=MARKDOWN_V2)
