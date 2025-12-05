import sys
sys.path.append("src/entities")

from entity import Entity

class Character(Entity):
    additional_prm = [
        "attributes_physical",
        "attributes_social",
        "attributes_mental",

        "abilities_talents",
        "abilities_skills",
        "abilities_knowledges",

        "willpower"
    ]

    Path = "local/characters"

    def __init__(self, id: int = 0, name="EMPTY_NAME", disc="EMPTY_DISCRIPTION", tags=[], 
                 attributes_physical=0, attributes_social=0, attributes_mental=0,
                 abilities_talents=0, abilities_skills=0, abilities_knowledges=0, willpower=0) -> None:
        super().__init__(id, name, disc, tags)
        self._attributes_physical = int(attributes_physical)
        self._attributes_social = int(attributes_social)
        self._attributes_mental = int(attributes_mental)
        self._abilities_talents = int(abilities_talents)
        self._abilities_skills = int(abilities_skills)
        self._abilities_knowledges = int(abilities_knowledges)
        self._willpower = int(willpower)

    @property
    def attributes_physical(self):
        return self._attributes_physical

    @property
    def attributes_social(self):
        return self._attributes_social

    @property
    def attributes_mental(self):
        return self._attributes_mental

    @property
    def abilities_talents(self):
        return self._abilities_talents

    @property
    def abilities_skills(self):
        return self._abilities_skills

    @property
    def abilities_knowledges(self):
        return self._abilities_knowledges

    @property
    def willpower(self):
        return self._willpower