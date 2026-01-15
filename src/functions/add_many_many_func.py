from src.entities import Item
from src.users import UserData
from src.functions import Function


class AddManyManyFunction(Function):
    def execute(self, user_data: UserData, num: int, items_and_counts = []):
        i = 0
        
        try:
            while i < num:
                item_id = items_and_counts[i*2]
                count = items_and_counts[i*2 + 1]
                user_data.AddItemToInventory(item_id, count)
                i += 1
        except:
            pass

