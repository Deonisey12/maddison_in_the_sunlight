import json, os


class Entity():
    base_prm = [
            "id",
            "name",
            "disc",
            "tags"
            ]

    additional_prm = []

    Path = "local/entity"
    
    def __init__(self, id, name="EMPTY NAME", disc="EMPTY DISCRIPTION", tags=[]) -> None:
        self._id = int(id)
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

    def _get_param_value(self, param: str):
        if hasattr(self, param):
            return getattr(self, param)
        private_param = f"_{param}"
        if hasattr(self, private_param):
            return getattr(self, private_param)
        return "N/A"

    def _format_param_value(self, value) -> str:
        if isinstance(value, list):
            return ", ".join(str(v) for v in value) if value else "[]"
        return str(value)

    def _to_string(self) -> str:
        info_lines = [f"_CLASS:_ {self.__class__.__name__}"]
        all_params = self.base_prm + self.additional_prm

        for param in all_params:
            value = self._get_param_value(param)
            formatted_value = self._format_param_value(value)
            param_line = f"_{param.upper()}:_ {formatted_value}"
            info_lines.append(param_line)
        
        return "\n".join(info_lines)

    def __str__(self) -> str:
        return self._to_string()

    def __repr__(self) -> str:
        return self._to_string()

    def IncId(self):
        self._id += 1

    @staticmethod
    def escape_markdown_v2(text: str) -> str:
        escape_chars = r'().!-'
        return ''.join(['\\' + char if char in escape_chars else char for char in text])

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
                args.append(Entity.escape_markdown_v2(str(json_dct[f"_{bp}"])))

            for ap in cls.additional_prm:
                args.append(Entity.escape_markdown_v2(str(json_dct[f"_{ap}"])))

            res = cls(*args)

            return res
        except Exception as ex:
            print(ex)
            return None
