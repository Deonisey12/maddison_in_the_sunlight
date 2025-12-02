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

    def SetId(self, id):
        self._id = id

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

    def SaveToJson(self):
        if self._id == 0:
            self._id = random.randint(100000, 999999)
            
            while True:
                if not os.path.exists(self.__filename):
                    break

                if self._id < 999999:
                    self._id += 1
                else:
                    self._id = random.randint(100000, 999999)

        os.makedirs(os.path.join(os.getcwd(), self._path), exist_ok=True)

        obj_js = json.dumps(self, default=lambda o: o.__dict__, ensure_ascii=False)

        file = open(self.__filename, "w")
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
            res.SetId(json_dct["_id"])

            return res
        except:
            return None
