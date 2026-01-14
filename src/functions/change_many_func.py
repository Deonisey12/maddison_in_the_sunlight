from src.entities import Item
from src.users import UserData
from src.functions import Function


class ChangeManyFunction(Function):
    def execute(self, user_data: UserData, from_item_id, to_item_id, from_count: int, to_count: int):
        if user_data.RmItemFromInventory(from_item_id, from_count):
            user_data.AddItemToInventory(to_item_id, to_count)
