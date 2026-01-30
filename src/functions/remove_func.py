from src.entities import Item
from src.users import UserData
from src.functions import Function


class RemoveFunction(Function):
    def execute(self, user_data: UserData, item_id) -> bool:
        return user_data.RmItemFromInventory(item_id)
