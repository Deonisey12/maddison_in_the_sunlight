from .add_func import AddFunction
from .remove_func import RemoveFunction
from .change_func import ChangeFunction
from .add_many_func import AddManyFunction
from .remove_many_func import RemoveManyFunction
from .change_many_func import ChangeManyFunction
from .challenge_func import ChallengeFunction
from .pay_challenge_func import PayChallengeFunction
from .relax_func import RelaxFunction

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

    def GetFunction(function_name: str):
        function_class = Functions.Functions.get(function_name, None)
        if function_class:
            return function_class()
        return None