from entities.database import Database

import telegram as tg
import telegram.ext as tgx

from base_form import BaseForm



class BotCommands():

    _base_form = BaseForm()

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
        
        request = ' '.join(update.message.text.split(' ')[1:])
        request = request.split('#')
        print(request)
        try:
            entity = self._gen.Create(*request)
            entity.SaveToJson()
            await update.message.reply_text("Создано")
        except Exception as ex:
            await update.message.reply_text(f"не удалось ({ex.__str__})")

    async def test_form(self, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE):
        text, rpm, prcm = self._base_form.GenerateLayout(
            self._database.GetEntityById("Scene", 0),
            [
                self._database.GetEntityById("Scene", 1),
                self._database.GetEntityById("Scene", 2)
            ]
        )
        
        await update.message.reply_text(
            text,
            reply_markup=rpm,
            parse_mode=prcm
        )


    async def button_callback(self, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        
        await query.edit_message_text(text=f"Selected option: {query.data}")
