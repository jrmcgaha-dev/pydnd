import typing


class Creature:

    _default_ac = 10
    _alignment_hash = {
        'l': 0,
        'g': 0,
        'n': 1,
        'c': 2,
        'e': 2,
        'u': 255,
    }

    def __init__(self):
        self.name: str = ''
        self.size: str = ''
        self.type: str = ''
        self.alignment: typing.Tuple[str, str] = ('', '')
        self.armor_class: int = 10
        self.hitpoints: int = 0
        self.speed: int = 0
        self.attributes: typing.Any = None
        # Attributes will eventually have custom handler class
        self.saving_throws: typing.List[str] = list()
        self.skills: typing.List[str] = list()
        self.damage_resistances: typing.List[str] = list()
        self.damage_vulnerabilities: typing.List[str] = list()
        self.damage_immunities: typing.List[str] = list()
        self.senses: typing.List[str] = list()
        self.languages: typing.List[str] = list()
