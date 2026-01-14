import sys
sys.path.append("src/entities")

from entity import Entity

class Event(Entity):
    additional_prm = [
        "function",
        "functionParams"
    ]

    Path = "local/events"

    def __init__(self, id: int = 0, name="EMPTY NAME", disc="EMPTY DISCRIPTION", tags=[], function = None, functionParams = []) -> None:
        super().__init__(id, name, disc, tags)
        self._function = function
        self._functionParams = functionParams

    @property
    def function(self):
        return self._function

    def ParameterRegistration(self):
        try:
            from functions import Functions
            self.Function = Functions.GetFunction(str(self._function))
            self.FunctionParams = []

            for i in str(self._functionParams).split(", "):
                self.FunctionParams.append(int(i))
        except Exception as ex:
            self.Function = None
            self.FunctionParams = []

    def Invoke(self, user_state):
        if (self.Function is not None):
            self.Function(user_state, *self.FunctionParams)