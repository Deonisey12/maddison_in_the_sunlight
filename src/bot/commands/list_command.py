import sys
sys.path.append("src/bot")

from entities.database import Database
from generators.generator import Generator
from generators.list import Entities
import telegram as tg
import telegram.ext as tgx

from base_form import BaseForm
from cmd_dictionary import UserData, Actions
from .base_command import BaseCommand


class ListCommand(BaseCommand):
    def __init__(self, database: Database):
        self._database = database
        self._base_form = BaseForm()
        self._gen = Generator()

    async def execute(self, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE):
        id = 0
        entities = []
        for ename in Entities:
            entities.append(self._gen.Create("Event", id, ename))
            id += 1

        layout = self._base_form.GenerateLayout(
            self._gen.Create("Scene", 0, "List Entity", "Выберите тип сущности"),
            entities,
            action=Actions.LIST
        )
        
        sent_message = await update.message.reply_text(
            layout.text,
            reply_markup=layout.reply_markup,
            parse_mode=layout.parce_mode
        )

