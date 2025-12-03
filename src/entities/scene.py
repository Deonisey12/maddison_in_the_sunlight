import sys
sys.path.append("src/entities")

from entity import Entity

class Scene(Entity):
    additional_prm = [
        "isGlobal",
        "img_path"
    ]

    def __init__(self, name, disc="empty", tags="", isGlobal=True, img=None) -> None:
        super().__init__(name, disc, tags)
        self._path = "local/scenes"
        self._isGlobal = isGlobal
        self._img_path = img