import sys
sys.path.append("src/bot")
sys.path.append("src/generators")

from generators.generator import Generator

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
        return self._generator.Create("Event", self.DELETE, "УДАЛИТЬ", "Delete entity")

    @property
    def BACK_BUTTON(self):
        return self._generator.Create("Event", self.BACK, "НАЗАД", "Back to list")

    @property
    def CLOSE_BUTTON(self):
        return self._generator.Create("Event", self.CLOSE, "ЗАКРЫТЬ", "Close list")

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
