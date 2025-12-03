import sys
sys.path.append("src/entities")

from entity import Entity

class Item(Entity):
    additional_prm = ["isUsable"]

    Path = "local/items"

    def __init__(self, name, disc="empty", tags="", isUsable=False) -> None:
        super().__init__(name, disc, tags)
        self._isUsable = isUsable

    @property
    def isUsable(self):
        return self._isUsable
        