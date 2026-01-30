from src.users import UserData
from src.functions import Function


class RelaxFunction(Function):
    def execute(self, user_data: UserData, amount: int) -> bool:
        raise NotImplementedError("RelaxFunction is not implemented")
