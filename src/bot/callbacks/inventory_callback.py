import sys
sys.path.append("src/bot")

import telegram as tg
import telegram.ext as tgx

from generators.generator import Generator
from commands.list_buttons import LC_Buttons

from .base_callback import BaseCallback
from cmd_dictionary import (
    MARKDOWN_V2,
    Actions,
    InventoryState,
    UserState,
    )

class InventoryCallback(BaseCallback):
    def __init__(self):
        self._generator = Generator()
        self._lc_buttons = LC_Buttons(self._generator)

    async def execute(self, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE, data: str):
        query = update.callback_query
        state = context.user_data.get(UserState.INVENTORY_STATE, {})

        if not state or not state.get(InventoryState.ACTIVE):
            return

        if int(data) in self._lc_buttons.get_button_ids():
            if int(data) == self._lc_buttons.CLOSE:
                state[InventoryState.ACTIVE] = False

                await query.edit_message_text(
                    "*Сумка*\n_ты закрываешь сумку_",
                    reply_markup=None,
                    parse_mode=MARKDOWN_V2
                )
                return

