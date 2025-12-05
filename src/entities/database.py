import sys
sys.path.append("src/generators")
sys.path.append("src/entities")

import os, json

from typing import Hashable
from generators.list import Entities
from generators.generator import Generator

class Database():

    _db: dict = {}
    _gen = Generator()

    def Load(self):
        for ename, etype in Entities.items():
            path = etype.Path
            
            try:
                files = os.listdir(os.path.join(os.getcwd(), path))
            except:
                files = []

            fdict = {}
            for f in files:
                id = int(f.split("_")[0].removeprefix("id"))
                fpath = os.path.join(path, f)
                fdict[id] = fpath

            self._db[ename] = fdict

    def db(self, class_name: str):
        return self._db[class_name]

    def CreateEntity(self, class_name: Hashable, *args, **kwargs):
        entity = self._gen.Create(class_name, *args, **kwargs)

        fdict = self._db[class_name]

        while fdict.get(entity.id) != None:
            entity.IncId()
        
        entity.SaveToJson()
        self._db[class_name][entity.id] = entity.shotfilename
        return entity

    def GetEntityById(self, class_name: str, id: int = None):
        if id == None:
            return None

        filepath = self._db[class_name].get(id)
        if filepath == None:
            return None
        
        with open(filepath, "r") as f:
            data = f.read()
            res = json.loads(data, object_hook=Entities[class_name].JsonDecoder)

        return res

    def DeleteEntityById(self, class_name: str, id: int = None):
        if id == None:
            return False

        filepath = self._db[class_name].get(id)
        if filepath == None:
            return False

        full_path = os.path.join(os.getcwd(), filepath)
        
        try:
            if os.path.exists(full_path):
                os.remove(full_path)
            del self._db[class_name][id]
            return True
        except Exception:
            return False

        