import sys
sys.path.append("src/generators")
sys.path.append("src/entities")

import os

from typing import Hashable, Callable
from typing_extensions import Dict
from generators.list import Entities
from generators.generator import Generator

class Database():

    _db: dict = {}
    _gen = Generator()

    def Load(self):
        for ename, etype in Entities.items():
            path = etype.Path
            files = os.listdir(os.path.join(os.getcwd(), path))

            fdict = {}
            for f in files:
                id = int(f.split("_")[0].removeprefix("id"))
                fpath = os.path.join(path, f)
                fdict[id] = fpath

            self._db[ename] = fdict


    def CreateEntity(self, class_name: Hashable, *args, **kwargs):
        entity = self._gen.Create(class_name, *args, **kwargs)

        fdict = self._db[class_name]

        while fdict.get(entity.id) != None:
            entity.IncId()
        
        entity.SaveToJson()
        self._db[class_name][entity.id] = entity.shotfilename
        print(self._db)

    def GetEntityById(self, id: int = None):
        if id == None:
            return None



        