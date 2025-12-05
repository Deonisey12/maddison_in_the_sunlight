import sys
sys.path.append("src/entities")

from entities.entity import Entity

import telegram as tg


class Layout():

    def __init__(self, text, reply_markup, parce_mode, img = None) -> None:
        self.text = text
        self.reply_markup = reply_markup
        self.parce_mode = parce_mode
        self.img = None


class BaseForm():
    _parce_mode = "MarkdownV2"

    def __init__(self):
        self.Clear()

    def Clear(self):
        self._reply_markup = None
        self._text = ""
        self._img = None

    def _generate_header(self, main_scene: Entity) -> str:
        return f"*{str(main_scene.name)}*"

    def _generate_body(self, main_scene: Entity) -> str:
        return f"{str(main_scene.disc)}"

    def GenerateLayout(self, main_scene: Entity, vars: Entity = [], action: str = None):
        if len(vars) < 1:
            raise ValueError
        self.Clear()
        
        keyboard = []
        for v in vars:
            if action:
                callback_data = f"{action}:{v.id}"
            else:
                callback_data = str(v.id)
            kbe = tg.InlineKeyboardButton(str(v.name), callback_data=callback_data)
            keyboard.append([kbe])

        self._reply_markup = tg.InlineKeyboardMarkup(keyboard)

        header = self._generate_header(main_scene)
        body = self._generate_body(main_scene)

        self._text = header + "\n" + body

        return Layout(self._text, self._reply_markup, self._parce_mode)
