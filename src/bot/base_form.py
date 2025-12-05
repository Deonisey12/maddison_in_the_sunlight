import sys
sys.path.append("src/entities")

from entities.scene import Scene

import telegram as tg
import telegram.ext as tgx


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

    def GenerateLayout(self, main_scene: Scene, vars: Scene = [], action: str = None):
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

        header = f"*{str(main_scene.name)}*\n"
        body = f"{str(main_scene.disc)}"

        self._text = header + body

        return Layout(self._text, self._reply_markup, self._parce_mode)



        

        

        

        

    