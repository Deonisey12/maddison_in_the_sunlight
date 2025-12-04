import sys
sys.path.append("src/bot")

import telegram as tg
import telegram.ext as tgx

from entities.database import Database
from generators.generator import Generator
from generators.list import Entities

from .base_callback import BaseCallback
from bot.cmd_dictionary import MARKDOWN_V2, Actions, ListState, UserData
from bot.base_form import BaseForm


class ListCallback(BaseCallback):
    def __init__(self, database: Database):
        self._database = database
        self._generator = Generator()
        self._base_form = BaseForm()

    async def execute(self, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE, data: str):
        query = update.callback_query
        state = context.user_data.get(UserData.LIST_STATE, {})

        if not state or not state.get(ListState.ACTIVE):
            return

        if state[ListState.TYPE] is None:

            type_key = list(Entities.keys())[int(data)]
            entity_ids = self._database.db(type_key)

            entities = []
            for e in entity_ids.keys():
                entity = self._database.GetEntityById(type_key, e)
                if entity:
                    entity_obj = self._generator.Load(type_key, entity.filename)
                    entities.append(entity_obj)
            
            layout = self._base_form.GenerateLayout(
                self._generator.Create("Scene", 0, "List Entity", f"Элементы списка {type_key}"),
                entities,
                action=Actions.LIST
            )

            state[ListState.TYPE] = type_key          
            await query.edit_message_text(
                layout.text,
                reply_markup=layout.reply_markup,
                parse_mode=layout.parce_mode
            )
            return

        if state[ListState.ENTITY] is None:
            entity = self._database.GetEntityById(state[ListState.TYPE], int(data))
            

            layout = self._base_form.GenerateLayout(
                entity,
                [
                    self._generator.Create("Event", 0, "Delete", "Event 1"),
                    self._generator.Create("Event", 1, "Back", "Event 2"),
                    self._generator.Create("Event", 2, "Close", "Event 3"),
                ],
                action=Actions.LIST
            )

            state[ListState.ENTITY] = entity

            await query.edit_message_text(
                layout.text,
                reply_markup=layout.reply_markup,
                parse_mode=layout.parce_mode
            )
            return

        if int(data) == 0:
            self._database.DeleteEntityById(state[ListState.TYPE], state[ListState.ENTITY].id)

        type_key = state[ListState.TYPE]
        state[ListState.ENTITY] = None
        state[ListState.TYPE] = None

        # if int(data) == 2:
        state[ListState.ACTIVE] = False
        await query.edit_message_text(
            "*List Entity*\nРедактирование завершено",
            reply_markup=None,
            parse_mode=MARKDOWN_V2
        )
        return

        #TODO: return first state of message
        