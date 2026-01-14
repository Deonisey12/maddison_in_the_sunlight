from src.entities import Item
from src.users import UserData
from src.functions import Function


class RemoveManyFunction(Function):
    def execute(self, user_data: UserData, item: Item, count: int):
        pass
