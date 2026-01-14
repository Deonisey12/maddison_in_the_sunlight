from src.entities import Item
from src.users import UserData
from src.functions import Function


class ChangeManyFunction(Function):
    def execute(self, user_data: UserData, from_item: Item, to_item: Item, from_count: int, to_count: int):
        pass
