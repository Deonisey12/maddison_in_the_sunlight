import sys
sys.path.append("src/entities")

from entities.scene import Scene

import telegram as tg
import telegram.ext as tgx


class BaseForm():
    _parce_mode = "MarkdownV2"

    def __init__(self):
        self.Clear()

    def Clear(self):
        self._reply_markup = None
        self._text = ""
        self._img = None
        
    @staticmethod
    def escape_markdown_v2(text: str) -> str:
        escape_chars = r'_*[]()~`>#+-=|{}.!'
        return ''.join(['\\' + char if char in escape_chars else char for char in text])

    def GenerateLayout(self, main_scene: Scene, vars: Scene = []):
        if len(vars) < 1:
            raise ValueError
        self.Clear()
        
        keyboard = []
        row = []
        for v in vars:
            kbe = tg.InlineKeyboardButton(str(v.name), callback_data=str(v.id))
            row.append(kbe)
        keyboard.append(row)
        self._reply_markup = tg.InlineKeyboardMarkup(keyboard)

        header = f"*{self.escape_markdown_v2(str(main_scene.name))}*\n"
        body = f"{self.escape_markdown_v2(str(main_scene.disc))}"

        self._text = header + body

        return self._text, self._reply_markup, self._parce_mode



        

        

        

        

    