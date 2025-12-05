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
from bot.commands.list_command import LC_Buttons


class ListCallback(BaseCallback):
    def __init__(self, database: Database):
        self._database = database
        self._generator = Generator()
        self._base_form = BaseForm()
        self._lc_buttons = LC_Buttons(self._generator)

    async def execute(self, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE, data: str):
        query = update.callback_query
        state = context.user_data.get(UserData.LIST_STATE, {})

        if not state or not state.get(ListState.ACTIVE):
            return

        type_key = None

        if int(data) in self._lc_buttons.get_button_ids():

            if int(data) == self._lc_buttons.BACK:
                if state[ListState.ENTITY] is None:
                    state[ListState.TYPE] = None
                    entities = self._generator.GetEntities()
                    entities.append(self._lc_buttons.CLOSE_BUTTON)

                    layout = self._base_form.GenerateLayout(
                        self._generator.Create("Scene", 0, "List Entity", "Выберите тип сущности"),
                        entities,
                        action=Actions.LIST
                    )
                else:
                    state[ListState.ENTITY] = None
                    layout = self.get_db_to_layout(state[ListState.TYPE])

                await query.edit_message_text(
                    layout.text,
                    reply_markup=layout.reply_markup,
                    parse_mode=layout.parce_mode
                )
                return


            if int(data) == self._lc_buttons.DELETE:
                self._database.DeleteEntityById(state[ListState.TYPE], state[ListState.ENTITY].id)

            type_key = state[ListState.TYPE]
            state[ListState.ENTITY] = None
            state[ListState.TYPE] = None    

            if int(data) == self._lc_buttons.CLOSE:
                state[ListState.ACTIVE] = False
                await query.edit_message_text(
                    "*List Entity*\nРедактирование завершено",
                    reply_markup=None,
                    parse_mode=MARKDOWN_V2
                )
                return

        if state[ListState.TYPE] is None:
            if type_key is None:
                type_key = list(Entities.keys())[int(data)]

            layout = self.get_db_to_layout(type_key)

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
                self._lc_buttons.get_buttons(),
                action=Actions.LIST
            )

            state[ListState.ENTITY] = entity

            await query.edit_message_text(
                layout.text,
                reply_markup=layout.reply_markup,
                parse_mode=layout.parce_mode
            )
            return

    

    def get_db_to_layout(self, type_key: str):
        entity_ids = self._database.db(type_key)

        if len(entity_ids) == 0:
            layout = self._base_form.GenerateLayout(
                self._generator.Create("Scene", 0, "List Entity", f"Нет элементов списка {type_key}"),
                [
                    self._lc_buttons.BACK_BUTTON, 
                    self._lc_buttons.CLOSE_BUTTON
                ],
                action=Actions.LIST
            )
        else:
            entities = []
            for e in entity_ids.keys():
                entity = self._database.GetEntityById(type_key, e)
                if entity:
                    entity_obj = self._generator.Load(type_key, entity.filename)
                    entities.append(entity_obj)

            entities.append(self._lc_buttons.BACK_BUTTON)
            entities.append(self._lc_buttons.CLOSE_BUTTON)
            
            layout = self._base_form.GenerateLayout(
                self._generator.Create("Scene", 0, "List Entity", f"Элементы списка {type_key}"),
                entities,
                action=Actions.LIST
            )

        return layout