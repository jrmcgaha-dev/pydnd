"""monster houses the Monster class and handles interaction with stored tables
from the 5e basic rules to handle simple calculations

"""
import json
import typing
from pkg_resources import resource_stream

from pydnd.ability_scores import Ability, AbilityScores
from pydnd.creature import Creature
from pydnd.dice_bag import Roller


class Monster(Creature):
    """The Monster class is a sub-class of Creature designed to interact with
    the unique math and properties of Monster entries in Dungeons and
    Dragons 5th edition.

    """
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
        """Monster initialization creates a new, empty Monster ready for
        assignment of information. Other than the following attributes,
        initialization is identical to pydnd.creature.Creature.__init__

        Manual Entry
        ------------
        challenge_rating : float
            Value that represents a monster's challenge rating
        hit_dice_number : int
            Value that represents the number of hit dice a monster has

        See Also
        --------
        pydnd.creature.Creature.__init__

        """
        self.challenge_rating: float = 0
        self.hit_dice_number: int = 1
        super().__init__()

    @property
    def experience(self) -> int:
        """Property that calculates the experience value for a creature based
        upon its challenge rating. The 5e table only accounts for whole
        number values up to CR 30. This property extends the calculation by
        estimating in-between challenge ratings (i.e. CR 5.5) and values
        greater than 30.

        Returns
        -------
        int
            Experience value of Monster

        """
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
        """Property that calculates the proficiency bonus of a monster.
        Monster proficiency bonuses are based on the monster's challenge
        rating.

        Returns
        -------
        int
            Proficiency bonus of Monster instance

        """
        return max((self.challenge_rating-1, 0))//4 + 2

    @property
    def avg_hp(self) -> int:
        """Property that calculates the average hitpoints for a monster.
        Monster hit die type is based on the monster's size and the total
        average value assumes average on all hit dice (i.e. 1d6 == 3.5) plus
        the monster's constitution modifier per hit die.

        Returns
        -------
        int
            Average hitpoints based on size and number of hit dice

        Notes
        -----
        While one could attempt to predict the scaling of hit dice greater
        than gargantuan (1d20 == 10.5), the excessive size already deviates
        from the norm enough that the average hitpoints should better serve
        as a guide rather than a hard and fast rule.

        """
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
