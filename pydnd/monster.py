import json
import typing
from pkg_resources import resource_stream

from pydnd.ability_scores import AbilityScores
from pydnd.creature import Creature
from pydnd.dice_bag import Roller


class Monster(Creature):
    _challenge_to_experience: typing.Dict[str, int] = json.load(
        resource_stream(
            "pydnd",
            "cr_to_xp.json"
        )
    )

    def __init__(self):
        self.challenge_rating: float = 0
        super().__init__()

    @property
    def experience(self) -> int:
        _int_part = int(self.challenge_rating)
        _dec_part = self.challenge_rating - _int_part
        _low = self._challenge_to_experience.get(str(min(_int_part, 30)), 0)
        if _int_part >= 30:
            _low += sum(val*100 for val in range(31, _int_part+1))
            _estimate = (_int_part+1) * 100
        else:
            _estimate = self._challenge_to_experience.get(str(_int_part+1), 0)
            _estimate -= _low
        return _low + round(_dec_part*_estimate)

    @property
    def proficiency(self) -> int:
        return max((self.challenge_rating-1, 0))//4 + 2
