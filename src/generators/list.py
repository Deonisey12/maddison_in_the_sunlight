import sys
sys.path.append("src/generators")

from generators import entity, item, scene
from typing import Hashable, Callable


Entities: dict[Hashable, Callable[..., entity.Entity]] = {
        "Entity": entity.Entity,
        "Item": item.Item,
        "Scene": scene.Scene
    }