import json
import sys
sys.path.append("src/bot")

import telegram as tg
import telegram.ext as tgx

from cmd_dictionary import Actions
from .base_command import BaseCommand
from entities.database import Database
from users.userdata import UserData
from forms import InventoryForm
from generators.generator import Generator
from .list_buttons import LC_Buttons

class InventoryCommand(BaseCommand):
    def __init__(self, database: Database):
        self._database = database
        self._inventory_form = InventoryForm()
        self._gen = Generator()
        self._list_buttons = LC_Buttons(self._gen)

    async def execute(self, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE):
        user_name = update.message.from_user.username
        user_data = UserData.LoadByName(user_name)

        quantities = list(user_data.inventory.values())
        quantities.append(0)

        entities = []
        for item in user_data.inventory:
            entity = self._database.GetEntityById('Item', int(item))
            entities.append(entity)
        entities.append(self._list_buttons.CLOSE_BUTTON)

        layout = self._inventory_form.GenerateLayout(
            self._gen.Create("Scene", 0, "Inventory", "Inventory"),
            entities,
            quantities,
            action=Actions.INVENTORY
        )

        await update.message.reply_text(layout.text, reply_markup=layout.reply_markup, parse_mode=layout.parce_mode)
        


