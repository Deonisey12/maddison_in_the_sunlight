import sys

from src.entities.item import Item
sys.path.append("src/bot")

import telegram as tg
import telegram.ext as tgx

from generators.generator import Generator
from commands.list_buttons import LC_Buttons

from .base_callback import BaseCallback
from forms import BaseForm, InventoryForm
from users.userdata import UserData
from cmd_dictionary import (
    MARKDOWN_V2,
    Actions,
    InventoryState,
    UserState,
    )

class InventoryCallback(BaseCallback):
    _USE = -99

    def __init__(self, database):
        self._database = database
        self._generator = Generator()
        self._base_form = BaseForm()
        self._inventory_form = InventoryForm()
        self._lc_buttons = LC_Buttons(self._generator)

    async def execute(self, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE, data: str):
        query = update.callback_query
        state = context.user_data.get(UserState.INVENTORY_STATE, {})

        if not state or not state.get(InventoryState.ACTIVE):
            await query.delete_message()
            return

        if int(data) == self._lc_buttons.CLOSE:
            state[InventoryState.ACTIVE] = False

            await query.edit_message_text(
                "*Сумка*\n_ты закрываешь сумку_",
                reply_markup=None,
                parse_mode=MARKDOWN_V2
            )
            return

        if state[InventoryState.ITEM_ID] != None:
            username = query.from_user.username
            user_state = UserData.LoadByName(username)

            if int(data) == self._USE:
                item: Item = self._database.GetEntityById('Item', state[InventoryState.ITEM_ID])
                item.Use(user_state)

            state[InventoryState.ITEM_ID] = None
            

            quantities = list(user_state.inventory.values())
            quantities.append(0)

            entities = []
            for item in user_state.inventory:
                entity = self._database.GetEntityById('Item', int(item))
                entities.append(entity)
            entities.append(self._lc_buttons.CLOSE_BUTTON)

            layout = self._inventory_form.GenerateLayout(
                self._generator.Create("Scene", 0, "Сумка", "Ты хлопаешь по карманам и заглядываешь в сумку\\."),
                entities,
                quantities,
                action=Actions.INVENTORY
            )
            await query.edit_message_text(
                layout.text,
                reply_markup=layout.reply_markup,
                parse_mode=layout.parce_mode
            )
            return

        state[InventoryState.ITEM_ID] = int(data)
        item: Item = self._database.GetEntityById('Item', int(data))

        buttons = []
        if item.isUsable == True:
            buttons.append(
                self._generator.Create('Entity', self._USE, 'Использовать')
            )
        buttons.append(self._lc_buttons.BACK_BUTTON)
        buttons.append(self._lc_buttons.CLOSE_BUTTON)

        layout = self._base_form.GenerateLayout(
                item,
                buttons,
                action=Actions.INVENTORY
            )
        await query.edit_message_text(
                    layout.text,
                    reply_markup=layout.reply_markup,
                    parse_mode=layout.parce_mode
                )
        return
            



