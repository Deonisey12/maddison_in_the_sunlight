from entities.database import Database
from generators.generator import Generator
from generators.list import Entities

import telegram as tg
import telegram.ext as tgx

from base_form import BaseForm, Layout




class BotCommands():

    _base_form = BaseForm()
    _gen = Generator()

    def __init__(self, database: Database):
        self._database = database

    async def start(self, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        await update.message.reply_html(
            rf"Hi {user.name}!"
        )

    async def help_command(self, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Help!")

    async def echo(self, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(update.message.text)

    async def create(self, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE):
        id = 0
        entyties = []
        for ename in Entities:
            entyties.append(self._gen.Create("Event", id, ename))
            id += 1

        layout = self._base_form.GenerateLayout(
            self._database.GetEntityById("Scene", 1),
            entyties
        )
        await update.message.reply_text(
            layout.text,
            reply_markup=layout.reply_markup,
            parse_mode=layout.parce_mode
        )


    async def test_form(self, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE):
        layout = self._base_form.GenerateLayout(
            self._database.GetEntityById("Scene", 0),
            [
                self._database.GetEntityById("Event", 0),
                self._database.GetEntityById("Event", 1),
            ]
        )
        
        await update.message.reply_text(
            layout.text,
            reply_markup=layout.reply_markup,
            parse_mode=layout.parce_mode
        )


    async def button_callback(self, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()

        type_key = list(Entities.keys())[int(query.data)]
        etype = Entities[type_key]

        ids = list(etype.base_prm + etype.additional_prm)

        state = {
            "active": True,
            "type": type_key,
            "ids": ids,
            "texts": [],
            "messages_to_delete": [],
        }
        context.user_data["create_state"] = state

        edited_message = await query.edit_message_text(text=f"Enter text for {type_key}")
        state["messages_to_delete"].append(edited_message.message_id)

        if state["ids"]:
            state["ids"].pop(0)  # Убираем id
        if state["ids"]:
            next_message = await query.message.reply_text(f"{state['ids'].pop(0)}")
            state["messages_to_delete"].append(next_message.message_id)

    async def message(self, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE):
        state = context.user_data.get("create_state")
        if not state or not state.get("active"):
            return

        text = update.message.text.strip()
        chat_id = update.message.chat_id
        user_message_id = update.message.message_id
        state["messages_to_delete"].append(user_message_id)

        if text.lower() == "cancel":
            await self._cleanup_messages(context.bot, chat_id, state.get("messages_to_delete", []))
            state["active"] = False
            state["texts"] = []
            state["ids"] = []
            await update.message.reply_text("Canceled")
            return

        if text.lower() == "eof":
            await self._finish_entity_creation(update, context, state, chat_id)
            return

        state["texts"].append(text)
        if len(state["ids"]) == 0:
            await self._finish_entity_creation(update, context, state, chat_id)
            return

        answer = f"*{state['ids'].pop(0)}*".upper()
        next_message = await update.message.reply_text(f"{answer}")
        state["messages_to_delete"].append(next_message.message_id)


    async def _finish_entity_creation(self, update, context, state, chat_id):

        e = self._database.CreateEntity(state["type"], 0, *state["texts"])
        await self._cleanup_messages(context.bot, chat_id, state.get("messages_to_delete", []))

        all_params = e.base_prm + e.additional_prm
        class_name = type(e).__name__

        info_lines = ["*CREATED ENTITY*"]
        info_lines.append(f"_CLASS:_ {class_name}")

        for param in all_params:
            value = getattr(e, param, None) or getattr(e, f"_{param}", "N/A")

            if isinstance(value, list):
                value = ", ".join(str(v) for v in value) if value else "[]"

            info_lines.append(f"_{param.upper()}:_ {value}")

        await update.message.reply_text("\n".join(info_lines), parse_mode="MarkdownV2")
        
        state["active"] = False
        state["texts"] = []
        state["ids"] = []
        state["messages_to_delete"] = []


    async def _cleanup_messages(self, bot, chat_id, message_ids):
        for msg_id in message_ids:
            try:
                await bot.delete_message(chat_id=chat_id, message_id=msg_id)
            except Exception:
                pass
