import sys
sys.path.append("src/entities")

from entity import Entity

class Item(Entity):
    additional_prm = ["isUsable"]

    Path = "local/items"

    def __init__(self, id: int=0, name="EMPTY NAME", disc="EMPTY DISCRIPTION", tags=[], isUsable=False) -> None:
        super().__init__(id, name, disc, tags)
        self._isUsable = isUsable

    @property
    def isUsable(self):
        return self._isUsable
        