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
        }
        context.user_data["create_state"] = state

        await query.edit_message_text(text=f"Enter text for {type_key}")

        if state["ids"]:
            state["ids"].pop(0)  # Убираем id
        if state["ids"]:
            await query.message.reply_text(f"{state['ids'].pop(0)}")

    async def message(self, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE):
        state = context.user_data.get("create_state")
        if not state or not state.get("active"):
            return

        text = update.message.text.strip()

        if text.lower() == "cancel":
            state["active"] = False
            state["texts"] = []
            state["ids"] = []
            await update.message.reply_text("Canceled")
            return

        if text.lower() == "eof":
            e = self._database.CreateEntity(state["type"], 0, *state["texts"])
            await update.message.reply_text(f"Entity created: {e}")
            state["active"] = False
            state["texts"] = []
            state["ids"] = []
            return

        state["texts"].append(text)

        if len(state["ids"]) == 0:
            e = self._database.CreateEntity(state["type"], 0, *state["texts"])
            await update.message.reply_text(f"Entity created: {e}")
            state["active"] = False
            state["texts"] = []
            state["ids"] = []
            return

        answer = f"{state['ids'].pop(0)}"
        await update.message.reply_text(f"{answer}")
