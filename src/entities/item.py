import sys
sys.path.append("src/entities")

from entity import Entity

class Item(Entity):
    additional_prm = [
        "isUsable",
        "function",
        "function_params"
        ]

    Path = "local/items"

    def __init__(self, id: int=0, name="EMPTY NAME", disc="EMPTY DISCRIPTION", tags=[], isUsable=False, function=None, function_params=[]) -> None:
        super().__init__(id, name, disc, tags)
        self._isUsable = isUsable
        self._function = function
        self._function_params = function_params

    @property
    def isUsable(self):
        return self._isUsable
        
    @property
    def function(self):
        return self._function