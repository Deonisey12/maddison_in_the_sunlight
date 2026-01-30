from src.entities import Item
from src.users import UserData
from src.functions import Function


class RemoveManyForceFunction(Function):
    def execute(self, user_data: UserData, item_id, count: int) -> bool:
        user_data.ForceRmItemFromInventory(item_id, count)
        return True