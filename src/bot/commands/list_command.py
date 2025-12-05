import sys
sys.path.append("src/bot")

from entities.database import Database
from generators.generator import Generator
from generators.list import Entities
import telegram as tg
import telegram.ext as tgx

from forms import BaseForm
from cmd_dictionary import ListState, UserData, Actions
from .base_command import BaseCommand

class LC_Buttons():

    def __init__(self, generator: Generator):
        self._generator = generator

    _delete = 1
    _back = 2
    _close = 3
    
    @property
    def DELETE(self):
        return -self._delete

    @property
    def BACK(self):
        return -self._back

    @property
    def CLOSE(self):
        return -self._close

    @property
    def DELETE_BUTTON(self):
        return self._generator.Create("Event", self.DELETE, "DELETE", "Delete entity")

    @property
    def BACK_BUTTON(self):
        return self._generator.Create("Event", self.BACK, "BACK", "Back to list")

    @property
    def CLOSE_BUTTON(self):
        return self._generator.Create("Event", self.CLOSE, "CLOSE", "Close list")

    def get_button_ids(self):
        return [
            self.DELETE,
            self.BACK,
            self.CLOSE,
        ]

    def get_buttons(self):
        return [
            self.DELETE_BUTTON,
            self.BACK_BUTTON,
            self.CLOSE_BUTTON,
        ]

class ListCommand(BaseCommand):
    def __init__(self, database: Database):
        self._database = database
        self._base_form = BaseForm()
        self._gen = Generator()
        self._lc_buttons = LC_Buttons(self._gen)

    async def execute(self, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE):
        entities = self._gen.GetEntities()
        entities.append(self._lc_buttons.CLOSE_BUTTON)

        layout = self._base_form.GenerateLayout(
            self._gen.Create("Scene", 0, "List Entity", "Выберите тип сущности"),
            entities,
            action=Actions.LIST
        )
        
        context.user_data[UserData.LIST_STATE] = {
            ListState.ACTIVE: True,
            ListState.TYPE: None,
            ListState.ENTITY: None
        }
        
        await update.message.reply_text(
            layout.text,
            reply_markup=layout.reply_markup,
            parse_mode=layout.parce_mode
        )

