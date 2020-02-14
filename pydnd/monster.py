import json
import typing
from pkg_resources import resource_stream

from pydnd.ability_scores import AbilityScores
from pydnd.creature import Creature
from pydnd.dice_bag import Roller


class Monster(Creature):
    _challenge_to_experience = json.load(
        resource_stream(
            "pydnd",
            "cr_to_xp.json"
        )
    )

    def __init__(self):
        self.challenge_rating: int = 0
        super().__init__()
