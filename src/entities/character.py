import sys
sys.path.append("src/entities")

from entity import Entity

class Character(Entity):
    additional_prm = [
        "attributesPhysical",
        "attributesSocial",
        "attributesMental",

        "abilitiesTalents",
        "abilitiesSkills",
        "abilitiesKnowledges",

        "willpower"
    ]

    Path = "local/characters"

    def __init__(self, id: int = 0, name="EMPTYNAME", disc="EMPTYDISCRIPTION", tags=[], 
                 attributesPhysical=0, attributesSocial=0, attributesMental=0,
                 abilitiesTalents=0, abilitiesSkills=0, abilitiesKnowledges=0, willpower=0) -> None:
        super().__init__(id, name, disc, tags)

        self._attributesPhysical = int(attributesPhysical)
        self._attributesSocial = int(attributesSocial)
        self._attributesMental = int(attributesMental)

        self._abilitiesTalents = int(abilitiesTalents)
        self._abilitiesSkills = int(abilitiesSkills)
        self._abilitiesKnowledges = int(abilitiesKnowledges)
        
        self._willpower = int(willpower)

    @property
    def attributesPhysical(self):
        return self._attributesPhysical

    @property
    def attributesSocial(self):
        return self._attributesSocial

    @property
    def attributesMental(self):
        return self._attributesMental

    @property
    def abilitiesTalents(self):
        return self._abilitiesTalents

    @property
    def abilitiesSkills(self):
        return self._abilitiesSkills

    @property
    def abilitiesKnowledges(self):
        return self._abilitiesKnowledges

    @property
    def willpower(self):
        return self._willpower