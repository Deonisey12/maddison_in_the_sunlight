import sys
sys.path.append("src/functions")

from functions import (
    AddFunction,
    RemoveFunction,
    ChangeFunction,
    AddManyFunction,
    RemoveManyFunction,
    ChangeManyFunction,
    ChallengeFunction,
    PayChallengeFunction,
    RelaxFunction,
)


class Functions:
    Functions = {
        "Add": AddFunction,
        "Remove": RemoveFunction,
        "Change": ChangeFunction,
        "AddMany": AddManyFunction,
        "RemoveMany": RemoveManyFunction,
        "ChangeMany": ChangeManyFunction,
        "Challenge": ChallengeFunction,
        "PayChallenge": PayChallengeFunction,
        "Relax": RelaxFunction,
    }

    def GetFunction(self, function_name: str):
        function_class = self.Functions.get(function_name, None)
        if function_class:
            return function_class.execute
        return None