import json
import os
import sys
sys.path.append("src/generators")

from typing import Hashable
from list import Entities

class ClassNotFoundError(ValueError):
    ...

class Generator():
    def Create(self, class_name: Hashable, *args, **kwargs):
        class_ret = Entities.get(class_name, None)
        if class_ret is not None:
            return class_ret(*args, **kwargs)
        
        raise ClassNotFoundError

    def Load(self, class_name: Hashable, filename: str):
        class_ret = Entities.get(class_name, None)
        if class_ret is not None:
            json_path = os.path.join(os.getcwd(), class_ret.Path, filename)
            with open(json_path, 'r') as f:
                json_data = json.loads(f.read())
            return class_ret.JsonDecoder(json_data)
        
        raise ClassNotFoundError

    def GetEntities(self):
        id = 0
        entities = []
        for ename in Entities:
            entities.append(self.Create("Event", id, ename))
            id += 1
        return entities