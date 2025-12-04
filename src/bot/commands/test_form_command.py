import sys
sys.path.append("src/bot")

from entities.database import Database
import telegram as tg
import telegram.ext as tgx

from base_form import BaseForm
from cmd_dictionary import UserData, Actions


class TestFormCommand:
    def __init__(self, database: Database):
        self._database = database
        self._base_form = BaseForm()

    async def execute(self, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE):
        layout = self._base_form.GenerateLayout(
            self._database.GetEntityById("Scene", 0),
            [
                self._database.GetEntityById("Event", 0),
                self._database.GetEntityById("Event", 1),
            ]
        )
        
        sent_message = await update.message.reply_text(
            layout.text,
            reply_markup=layout.reply_markup,
            parse_mode=layout.parce_mode
        )
        
        if UserData.FORM_ACTIONS not in context.user_data:
            context.user_data[UserData.FORM_ACTIONS] = {}
        context.user_data[UserData.FORM_ACTIONS][sent_message.message_id] = Actions.FORM

