import sys
sys.path.append("src/bot")

from generators.list import Entities
import telegram as tg
import telegram.ext as tgx

from cmd_dictionary import UserData, State, MARKDOWN_V2
from .base_callback import BaseCallback


class CreateCallback(BaseCallback):
    async def execute(self, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE, data: str):
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

