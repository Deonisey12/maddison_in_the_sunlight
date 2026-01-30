from src.entities import Item
from src.users import UserData
from src.functions import Function


class AddFunction(Function):
    def execute(self, user_data: UserData, item_id) -> bool:
        user_data.AddItemToInventory(item_id)
        return True
