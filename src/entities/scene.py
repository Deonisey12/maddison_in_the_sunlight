import sys
sys.path.append("src/entities")

from entity import Entity

class Scene(Entity):
    additional_prm = [
        "isGlobal",
        "img_path"
    ]

    Path = "local/scenes"

    def __init__(self,id: int=0, name="EMPTY NAME", disc="EMPTY DISCRIPTION", tags=[], isGlobal=True, img=None) -> None:
        super().__init__(id, name, disc, tags)
        self._isGlobal = isGlobal
        self._img_path = img

    @property
    def isGlobal(self):
        return self._isGlobal

    @property
    def img_path(self):
        return self._img_path