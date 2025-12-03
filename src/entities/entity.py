from inspect import Parameter
import json, os
import random


class Entity():
    base_prm = [
            "id",
            "name",
            "disc",
            "tags"
            ]

    additional_prm = []

    Path = "local/entity"
    
    def __init__(self, id: int=0, name="EMPTY_NAME", disc="EMPTY_DISCRIPTION", tags=[]) -> None:
        self._id = id
        self._name = name
        self._disc = disc
        self._tags = tags
        self._path = self.Path

    @property
    def id(self):
        return self._id
    @property
    def name(self):
        return self._name
    @property
    def disc(self):
        return self._disc
    @property
    def tags(self):
        return self._tags

    @property
    def shotfilename(self):
        fname = '_'.join((str(self._name)).lower().split(' '))
        return os.path.join(self._path, f"id{self._id}_{fname}")

    @property
    def filename(self):
            return os.path.join(os.getcwd(), self.shotfilename)

    def __repr__(self) -> str:
        res = f"<{self.__class__.__name__}__id{self._id}_{self._name}: \"{self._disc}\""
        for ap in self.additional_prm:            
            try:
                res += f", {ap}:{getattr(self, f"_{self.__class__.__name__}__{ap}")}"
            except:
                continue
            
        res += ">"
        return res

    def IncId(self):
        self._id += 1

    def SaveToJson(self):
        os.makedirs(os.path.join(os.getcwd(), self._path), exist_ok=True)

        obj_js = json.dumps(self, default=lambda o: o.__dict__, ensure_ascii=False)

        file = open(self.filename, "w")
        file.write(obj_js)
        file.close()

    @classmethod
    def JsonDecoder(cls, json_dct):
        try:
            args = []
            for bp in cls.base_prm:
                args.append(json_dct[f"_{bp}"])

            for ap in cls.additional_prm:
                args.append(json_dct[f"_{ap}"])

            res = cls(*args)

            return res
        except Exception as ex:
            print(ex)
            return None
