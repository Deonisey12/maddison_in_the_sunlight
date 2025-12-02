import sys
sys.path.append("src/generators")

from entity import Entity

class Item(Entity):
    additional_prm = ["isUsable"]

    def __init__(self, name, disc="empty", isUsable=False) -> None:
        super().__init__(name, disc)
        self._path = "local/items"
        self._isUsable = isUsable
        