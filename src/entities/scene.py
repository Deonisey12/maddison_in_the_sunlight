import sys
sys.path.append("src/entities")

from entity import Entity

class Scene(Entity):
    additional_prm = [
        "events",
        "isGlobal",
        "imgPath"
    ]

    Path = "local/scenes"

    def __init__(self,id: int=0, name="EMPTY NAME", disc="EMPTY DISCRIPTION", tags=[], events = "", isGlobal=True, img=None) -> None:
        super().__init__(id, name, disc, tags)

        if type(isGlobal == str):
            if isGlobal == 'True':
                self._isGlobal = True
            else:
                self._isGlobal = False
        else:
            self._isGlobal = isGlobal
        
        self._imgPath = img
        if img == "None":
            self._imgPath = None
        self._events = []
        if events != "":
            events = events[1:-1]
            for e in events.split(', '):
                self._events.append(int(e))

    @property
    def events(self):
        return self._events

    @property
    def isGlobal(self):
        return self._isGlobal

    @property
    def imgPath(self):
        return self._imgPath