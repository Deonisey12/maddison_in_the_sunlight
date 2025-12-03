import sys
sys.path.append("src/entities")

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