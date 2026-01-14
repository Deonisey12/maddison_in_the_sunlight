import sys
sys.path.append("src/entities")
from entity import Entity


class Item(Entity):
    additional_prm = [
        "isUsable",
        "function",
        "functionParams"
        ]

    Path = "local/items"

    def __init__(self, id: int=0, name="EMPTY NAME", disc="EMPTY DISCRIPTION", tags=[], isUsable=False, function=None, functionParams=[]) -> None:
        super().__init__(id, name, disc, tags)
        
        if type(isUsable == str):
            if isUsable == 'True':
                self._isUsable = True
            else:
                self._isUsable = False
        else:
            self._isUsable = isUsable

        self._function = function
        self._functionParams = functionParams

        self.ParameterRegistration()

    @property
    def isUsable(self):
        return self._isUsable
        
    @property
    def function(self):
        return self._function

    def ParameterRegistration(self):
        if self._isUsable:
            try:
                sys.path.append("src/functions")
                from functions import Functions

                self.Function = Functions.GetFunction(str(self._function))
                self.FunctionParams = []

                if not self._functionParams or self._functionParams == []:
                    return

                for i in str(self._functionParams).split(", "):
                    self.FunctionParams.append(int(i))
            except Exception as ex:
                self.Function = None
                self.FunctionParams = []

    def Use(self, user_data):
        if (self._isUsable) and (self.Function is not None):
            self.Function.execute(user_data, *self.FunctionParams)