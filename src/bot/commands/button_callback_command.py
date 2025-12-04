import sys
sys.path.append("src/bot")

from entities.database import Database
from generators.generator import Generator
from generators.list import Entities
import telegram as tg
import telegram.ext as tgx

from base_form import BaseForm
from cmd_dictionary import UserData, Actions, State, MARKDOWN_V2


class ButtonCallbackCommand:
    def __init__(self, database: Database):
        self._database = database
        self._base_form = BaseForm()
        self._gen = Generator()

    async def execute(self, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()

        message_id = query.message.message_id
        form_actions = context.user_data.get(UserData.FORM_ACTIONS, {})
        action = form_actions.get(message_id, Actions.CREATE)
        callback_data = query.data

        if action == Actions.CREATE:
            await self._handle_create_callback(update, context, callback_data)
        elif action == Actions.FORM:
            await self._handle_form_callback(update, context, callback_data)
        else:
            await query.edit_message_text(text=f"Неизвестное действие: {action}")

    async def _handle_create_callback(self, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE, data: str):
        query = update.callback_query
        
        type_key = list(Entities.keys())[int(data)]
        etype = Entities[type_key]

        ids = list(etype.base_prm + etype.additional_prm)

        state = {
            State.ACTIVE: True,
            State.TYPE: type_key,
            State.IDS: ids,
            State.TEXTS: [],
            State.MESSAGES_TO_DELETE: [],
        }
        context.user_data[UserData.CREATE_STATE] = state

        edited_message = await query.edit_message_text(text=f"Заполните параметры для {type_key}", parse_mode=MARKDOWN_V2)
        state[State.MESSAGES_TO_DELETE].append(edited_message.message_id)

        if state[State.IDS]:
            state[State.IDS].pop(0)
        if state[State.IDS]:
            next_message = await query.message.reply_text(f"*{state[State.IDS].pop(0)}*".upper(), parse_mode=MARKDOWN_V2)
            state[State.MESSAGES_TO_DELETE].append(next_message.message_id)

    async def _handle_form_callback(self, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE, data: str):
        query = update.callback_query
        
        entity_id = int(data)
        entity = self._database.GetEntityById("Event", entity_id)
        
        if entity:
            escaped_name = BaseForm.escape_markdown_v2(str(entity.name))
            escaped_disc = BaseForm.escape_markdown_v2(str(entity.disc))
            entity_info = f"*{escaped_name}*\n\n{escaped_disc}"
            await query.edit_message_text(text=entity_info, parse_mode=MARKDOWN_V2)
        else:
            await query.edit_message_text(text="Сущность не найдена")

