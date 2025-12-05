import sys
sys.path.append("src/bot")

from entities.database import Database
import telegram as tg
import telegram.ext as tgx

from forms.base_form import BaseForm
from cmd_dictionary import UserData, Actions
from .base_command import BaseCommand


class TestFormCommand(BaseCommand):
    def __init__(self, database: Database):
        self._database = database
        self._base_form = BaseForm()

    async def execute(self, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE):
        layout = self._base_form.GenerateLayout(
            self._database.GetEntityById("Scene", 0),
            [
                self._database.GetEntityById("Event", 0),
                self._database.GetEntityById("Event", 1),
            ],
            action=Actions.TEST_FORM
        )
        
        sent_message = await update.message.reply_text(
            layout.text,
            reply_markup=layout.reply_markup,
            parse_mode=layout.parce_mode
        )

