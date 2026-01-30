from src.entities import Item
from src.users import UserData
from src.functions import Function

class ChangeFunction(Function):
    def execute(self, user_data: UserData, from_item_id, to_item_id):
        if user_data.RmItemFromInventory(from_item_id):
            user_data.AddItemToInventory(to_item_id)
            return True
        return False
