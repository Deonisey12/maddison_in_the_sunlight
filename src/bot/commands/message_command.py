import sys
sys.path.append("src/bot")

from entities.database import Database
import telegram as tg
import telegram.ext as tgx

from base_form import BaseForm
from cmd_dictionary import UserData, CreateState, MARKDOWN_V2
from .base_command import BaseCommand


class MessageCommand(BaseCommand):
    def __init__(self, database: Database):
        self._database = database
        self._base_form = BaseForm()

    async def execute(self, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE):
        state = context.user_data.get(UserData.CREATE_STATE)
        if not state or not state.get(CreateState.ACTIVE):
            return

        text = update.message.text.strip()
        chat_id = update.message.chat_id
        user_message_id = update.message.message_id
        state[CreateState.MESSAGES_TO_DELETE].append(user_message_id)

        if text.lower() == "cancel":
            await self._cleanup_messages(context.bot, chat_id, state.get(CreateState.MESSAGES_TO_DELETE, []))
            state[CreateState.ACTIVE] = False
            state[CreateState.TEXTS] = []
            state[CreateState.IDS] = []
            await update.message.reply_text("Canceled")
            return

        if text.lower() == "eof":
            await self._finish_entity_creation(update, context, state, chat_id)
            return

        state[CreateState.TEXTS].append(text)
        if len(state[CreateState.IDS]) == 0:
            await self._finish_entity_creation(update, context, state, chat_id)
            return

        id_value = str(state[CreateState.IDS].pop(0)).upper()
        answer = f"*{id_value}*"
        next_message = await update.message.reply_text(f"{answer}", parse_mode=MARKDOWN_V2)
        state[CreateState.MESSAGES_TO_DELETE].append(next_message.message_id)

    async def _finish_entity_creation(self, update, context, state, chat_id):
        e = self._database.CreateEntity(state[CreateState.TYPE], 0, *state[CreateState.TEXTS])
        await self._cleanup_messages(context.bot, chat_id, state.get(CreateState.MESSAGES_TO_DELETE, []))

        all_params = e.base_prm + e.additional_prm
        class_name = type(e).__name__

        info_lines = ["*CREATED ENTITY*"]
        info_lines.append(f"_CLASS:_ {class_name}")

        for param in all_params:
            value = getattr(e, param, None) or getattr(e, f"_{param}", "N/A")

            if isinstance(value, list):
                value = ", ".join(str(v) for v in value) if value else "[]"
            
            info_lines.append(f"_{param.upper()}:_ {str(value)}")

        await update.message.reply_text("\n".join(info_lines), parse_mode=MARKDOWN_V2)
        
        state[CreateState.ACTIVE] = False
        state[CreateState.TEXTS] = []
        state[CreateState.IDS] = []
        state[CreateState.MESSAGES_TO_DELETE] = []

    async def _cleanup_messages(self, bot, chat_id, message_ids):
        for msg_id in message_ids:
            try:
                await bot.delete_message(chat_id=chat_id, message_id=msg_id)
            except Exception:
                pass

