import sys
sys.path.append("src/generators")

from entity import Entity

class Scene(Entity):
    additional_prm = [
        "isGlobal"
    ]

    def __init__(self, name, disc="empty", tags="", isGlobal=True) -> None:
        super().__init__(name, disc, tags)
        self._path = "local/scenes"
        self._isGlobal = isGlobal