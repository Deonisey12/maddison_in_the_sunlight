from src.entities import Item
from src.users import UserData
from src.functions import Function


class RemoveManyFunction(Function):
    def execute(self, user_data: UserData, item_id, count: int) -> bool:
        return user_data.RmItemFromInventory(item_id, count)
