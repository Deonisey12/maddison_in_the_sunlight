import sys
sys.path.append("src/entities")

from entity import Entity

class Item(Entity):
    additional_prm = ["isUsable"]

    def __init__(self, name, disc="empty", tags="", isUsable=False) -> None:
        super().__init__(name, disc, tags)
        self._path = "local/items"
        self._isUsable = isUsable
        