import json
import sys

import telegram as tg
import telegram.ext as tgx

from .base_command import BaseCommand
from entities.database import Database
from src.users.userdata import UserData

class InventoryCommand(BaseCommand):
    def __init__(self, database: Database):
        self._database = database

    async def execute(self, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE):
        user_name = update.message.from_user.username
        with open(f"local/users/{user_name}.json", "r") as f:
            data = f.read()
            js_data = json.loads(data)
            user_data = UserData.JsonDecoder(js_data)
        
        for item in user_data.inventory:
            print(self._database.GetEntityById(int(item)))


