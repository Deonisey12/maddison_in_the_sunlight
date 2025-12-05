import sys
sys.path.append("src/entities")

from entity import Entity

class Event(Entity):
    additional_prm = [
    ]

    Path = "local/events"

    def __init__(self, id: int = 0, name="EMPTY NAME", disc="EMPTY DISCRIPTION", tags=[]) -> None:
        super().__init__(id, name, disc, tags)