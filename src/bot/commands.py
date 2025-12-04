from entities.database import Database
from generators.generator import Generator
from generators.list import Entities

import telegram as tg
import telegram.ext as tgx

from base_form import BaseForm, Layout




class BotCommands():

    _base_form = BaseForm()
    _gen = Generator()

    _flag = False

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
        
        self._flag = True
        self._type = list(Entities.keys())[int(query.data)]

        await query.edit_message_text(text=f"Wait EOF")

    texts = []
    async def message(self, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE):
        if not self._flag:
            return
        
        text = update.message.text

        if text.lower() == "eof":
            e = self._database.CreateEntity(self._type, 0, *self.texts)
            await update.message.reply_html(
                rf"""
                <b>id{e.id}</b> {e.name}
                {e.disc}
                """
            )
            self._flag = False
            self.texts = []
            return
        
        if text.lower() == "cancel":
            self._flag = False
            self.texts = []
            await update.message.reply_text("Canceled")
            return

        self.texts.append(text)
