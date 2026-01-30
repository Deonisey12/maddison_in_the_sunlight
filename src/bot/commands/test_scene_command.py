import sys
sys.path.append("src/bot")

from entities.database import Database
import telegram as tg
import telegram.ext as tgx

from forms.base_form import BaseForm
from cmd_dictionary import SceneState, UserState, Actions
from .base_command import BaseCommand

from .create_scene_command import CreateSceneCommand


class TestSceneCommand(BaseCommand):
    def __init__(self, database: Database):
        self._database = database
        self._base_form = BaseForm()
        self.cs = CreateSceneCommand(database)

    async def execute(self, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE):
        self.cs.Scene = 0
        await self.cs.execute(update, context)

