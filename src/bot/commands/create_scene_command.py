import sys
sys.path.append("src/bot")

from entities.database import Database
import telegram as tg
import telegram.ext as tgx

from users.userdata import UserData
from forms.base_form import BaseForm
from cmd_dictionary import FormState, UserState, Actions
from .base_command import BaseCommand


class CreateSceneCommand(BaseCommand):
    def __init__(self, database: Database):
        self._database = database
        self._base_form = BaseForm()

        self.scene = -1

    @property
    def Scene(self):
        return self.scene

    @Scene.setter
    def Scene(self, value: int):
        self.scene = value

    def ReadUserScene(self, user_name):
        user_state = UserData.LoadByName(user_name)
        self.scene = user_state.Scene

    async def execute(self, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE):
        if(self.scene == -1):
            self.scene = 0
        
        test_scene = self._database.GetEntityById("Scene", self.Scene)
        events = []
        for e in test_scene.events:
            events.append(self._database.GetEntityById("Event", e))

        layout = self._base_form.GenerateLayout(
            test_scene,
            events,
            action=Actions.FORM
        )

        context.user_data[UserState.FORM_STATE] = {
            FormState.ACTIVE: True
        }

        try:
            if update.message:
                await update.message.reply_text(
                    layout.text,
                    reply_markup=layout.reply_markup,
                    parse_mode=layout.parce_mode
                )
            else:
                await update.callback_query.edit_message_text(
                    layout.text,
                    reply_markup=layout.reply_markup,
                    parse_mode=layout.parce_mode
                )
        except:
            pass
