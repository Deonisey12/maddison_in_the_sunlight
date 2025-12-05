import sys
sys.path.append("src/entities")

from entities.entity import Entity
from .base_form import BaseForm


class EntityForm(BaseForm):
    
    def _generate_header(self, main_scene: Entity) -> str:
        return f"*{str(main_scene.name)}*"

    def _generate_body(self, main_scene: Entity) -> str:
        return f"{str(main_scene)}"