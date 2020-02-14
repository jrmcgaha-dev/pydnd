import json
import typing
from pkg_resources import resource_stream

from pydnd.ability_scores import Ability, AbilityScores
from pydnd.creature import Creature
from pydnd.dice_bag import Roller


class Monster(Creature):
    _challenge_to_experience: typing.Dict[str, int] = json.load(
        resource_stream(
            "pydnd",
            "cr_to_xp.json"
        )
    )
    _size_mult_to_hp = {
        0.5: 2.5,
        2: 5.5,
        4: 6.5,
        8: 10.5
    }

    def __init__(self):
        self.challenge_rating: float = 0
        self.hit_dice_number: int = 1
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

    @property
    def avg_hp(self) -> int:
        if self.size_multiplier == 1:
            _die_val = 4.5
            if 'small' in self.size.lower():
                _die_val -= 1
        elif self.size_multiplier > 8:
            _die_val = 10.5
        else:
            _die_val = self._size_mult_to_hp.get(self.size_multiplier)
        _dice_hp = int(_die_val*self.hit_dice_number)
        _con_hp = self.hit_dice_number * self.attributes['con'].modifier
        return _dice_hp + _con_hp
