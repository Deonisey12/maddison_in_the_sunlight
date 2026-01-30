from src.entities import Event
from src.users import UserData
from src.functions import Function


class ChallengeFunction(Function):
    def execute(self, user_data: UserData, attribute, ability, difficulty: int, success_event: Event, fault_event: Event) -> bool:
        raise NotImplementedError("ChallengeFunction is not implemented")
