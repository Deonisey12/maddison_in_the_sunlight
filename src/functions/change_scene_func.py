from src.entities import Location
from src.users import UserData
from src.functions import Function

class ChangeSceneFunction(Function):
    def execute(self, user_data: UserData, scene_id: int, cost_item_id: int = -1, cost_count: int = 1) -> bool:
        if cost_item_id != -1:
            if user_data.RmItemFromInventory(cost_item_id, cost_count):
                user_data.Scene = scene_id
                return True
            return False
        else:
            user_data.Scene = scene_id
            return True