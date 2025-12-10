import sys
sys.path.append("src/entities")
sys.path.append("src/functions")

from entity import Entity
from functions import Functions


class Item(Entity):
    additional_prm = [
        "isUsable",
        "function",
        "functionParams"
        ]

    Path = "local/items"

    def __init__(self, id: int=0, name="EMPTY NAME", disc="EMPTY DISCRIPTION", tags=[], isUsable=False, function=None, functionParams=[]) -> None:
        super().__init__(id, name, disc, tags)
        self._isUsable = isUsable
        self._function = function
        self._functionParams = functionParams

    @property
    def isUsable(self):
        return self._isUsable
        
    @property
    def function(self):
        return self._function

    def ParameterRegistration(self):
        try:
            self.Function = Functions.GetFunction(str(self._function))
            self.FunctionParams = []

            for i in str(self._functionParams).split(", "):
                self.FunctionParams.append(int(i))
        except Exception as ex:
            self.Function = None
            self.FunctionParams = []