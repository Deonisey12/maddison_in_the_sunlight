from inspect import Parameter
import json, os
import random


class Entity():
    base_prm = [
            "name",
            "disc",
            "tags"
            ]

    additional_prm = []

    def __init__(self, name, disc="empty", tags=[]) -> None:
        self._name = name
        self._id = 0
        self._disc = disc
        self._path = "local/entity"
        self._tags = tags

    @property
    def __filename(self):
            fname = '_'.join((str(self._name)).lower().split(' '))
            return os.path.join(os.getcwd(), self._path, 
                        f"{fname}_id{self._id}")

    def __repr__(self) -> str:
        res = f"<{self.__class__.__name__}__{self._name}_id{self._id}: \"{self._disc}\""
        for ap in self.additional_prm:            
            try:
                res += f", {ap}:{getattr(self, f"_{self.__class__.__name__}__{ap}")}"
            except:
                continue
            
        res += ">"
        return res
    