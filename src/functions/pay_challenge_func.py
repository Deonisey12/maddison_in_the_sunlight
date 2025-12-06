from src.entities import Item, Event
from src.users import UserData


class PayChallengeFunction:
    def execute(self, user_data: UserData, attribute, ability, difficulty: int, cost_item: Item, count: int, success_event: Event, fault_event: Event):
        pass
