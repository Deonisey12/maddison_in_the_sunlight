import sys
sys.path.append("src/bot")

from entities.database import Database
import telegram as tg
import telegram.ext as tgx

from forms.base_form import BaseForm
from cmd_dictionary import FormState, UserState, Actions
from .base_command import BaseCommand


class TestFormCommand(BaseCommand):
    def __init__(self, database: Database):
        self._database = database
        self._base_form = BaseForm()

    async def execute(self, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE):
        test_scene = self._database.GetEntityById("Scene", 0)
        user_name = update.message.from_user.username

        events = []
        for e in test_scene.events:
            events.append(self._database.GetEntityById("Event", e))

        layout = self._base_form.GenerateLayout(
            test_scene,
            events,
            action=Actions.FORM
        )

        context.user_data[UserState.FORM_STATE] = {
            FormState.ACTIVE: True,
            FormState.USER_NAME: user_name
        }
        
        await update.message.reply_text(
            layout.text,
            reply_markup=layout.reply_markup,
            parse_mode=layout.parce_mode
        )

