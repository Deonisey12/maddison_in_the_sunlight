from .base_form import BaseForm
from entities.entity import Entity

import telegram as tg

class InventoryForm(BaseForm):

    def _generate_keyboard(self, vars: Entity = [], action: str = None):
        keyboard = []
        i = 0
        for v in vars:
            if action:
                callback_data = f"{action}:{v.id}"
            else:
                callback_data = str(v.id)
            kbe = tg.InlineKeyboardButton(f"{str(v.name)} x{self.numb[i]}", callback_data=callback_data)
            keyboard.append([kbe])
            i += 1
        return tg.InlineKeyboardMarkup(keyboard)

    def GenerateLayout(self, main_scene: Entity, vars: Entity = [], numb = [], action: str = None):
        self.numb = numb
        return super().GenerateLayout(main_scene, vars, action)
