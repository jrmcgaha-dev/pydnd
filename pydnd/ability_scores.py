"""ability_scores manages individual ability scores using the Ability class
and ability score arrays using the AbilityScores class
"""
from collections import defaultdict
import logging
import typing

from pydnd.dice_bag import Roller, _log as _roll_log
from pydnd.exceptions import AbilityError


_log = logging.getLogger(__name__)


class Ability:
    """Ability manages individual scores
    """

    _default_score = 10
    _details_formatter = ("Base\n"
                          "\t{base}\n"
                          "Permanent\n"
                          "\t{permanent}\n"
                          "Temporary\n"
                          "\t{temporary}\n"
                          "Overrides\n"
                          "\t{overrides}")

    def __init__(self, score: int = None, **permanent_modifiers):
        """Score and permanent modifiers may be declared on initialization or
        set later

        Parameters
        ----------
        score : int, optional
            The base value for the score before any modifiers (default: 10)
        permanent_modifiers : Dict[str, int], optional
            Various permanent modifiers to the score. These should be provided
            as keyword arguments in the style of type=value
            (ex. racial=2)

        Notes
        -----
        The Ability class natively handles the base score and permanent
        modifiers only. Properties for calculating temporary modifiers and
        override scores are provided to allow functionality with other
        methods/classes better designed to handle managing the existence of
        those modifiers.
        """
        if score is None:
            score = self._default_score
        self._base_score = score
        _log.debug("set _base_score = %r", self._base_score)
        self._mod_permanent = dict(**permanent_modifiers)
        _log.debug("set _mod_permanent = %r", self._mod_permanent)
        self._mod_temporary = defaultdict(list)
        self._mod_override = dict()

    def __call__(self) -> typing.Tuple[int, int]:
        """Provides easy access to score and modifier properties

        Returns
        -------
        Tuple[int, int]
            Provided in form of (score, modifier)

        """
        return self.score, self.modifier

    def __str__(self) -> str:
        """Produces a prettified string representation of the ability

        Returns
        -------
        str
            Provided in form "base[+temporary= total]|override (modifier)"
        """
        _base = self._base_score + sum(self._mod_permanent.values())
        _log.debug("str _base == %r", _base)
        if self._override > _base:
            return f"{self._override}<Override> ({self.modifier:+})"
        if self._temp_total:
            return (f"{_base}"
                    f"{self._temp_total:+}<Temp>"
                    f"= {_base+self._temp_total} "
                    f"({self.modifier:+})")
        return f"{_base} ({self.modifier:+})"

    @property
    def score(self) -> int:
        """Accesses score property getter and setter

        Parameters
        ----------
        value : int
            Sets base score to value and clears permanent modifiers

        Returns
        -------
        int
            Value of score plus any modifiers or override

        """
        _base = self._base_score + sum(self._mod_permanent.values())
        return max(_base+self._temp_total, self._override)

    @score.setter
    def score(self, value: int) -> typing.NoReturn:
        self._base_score = value
        self._mod_permanent = dict()

    @property
    def modifier(self) -> int:
        """Access modifier property getter

        Returns
        -------
        int
            Value of modifier based upon value of score property

        """
        return self.score//2 - 5

    @property
    def _temp_total(self) -> int:
        if any(self._mod_temporary.values()):
            return sum(map(max, self._mod_temporary.values()))
        return 0

    @property
    def _override(self) -> int:
        if any(self._mod_override.values()):
            return max(self._mod_override.values())
        return -255

    def add_permanent_modifier(self,
                               mods: typing.Dict = None,
                               **kwarg_mods) -> typing.NoReturn:
        """
        Adds permanent modifiers to the score. Permanent modifiers
        include racial additions, points from leveling, bonuses from
        wishes, and any other modification that is fundamentally a part
        of the ability.

        Parameters
        ----------
        mods: dict
            modifiers in a dict of form {mod_name: mod}
        kwarg_mods
            modifiers as keyword args in form name=mod
        """
        _log.debug("Before addition: %r", self._mod_permanent)
        if mods is not None:
            self._mod_permanent.update(mods)
        if kwarg_mods:
            self._mod_permanent.update(kwarg_mods)
        _log.debug("After addition: %r", self._mod_permanent)

    @property
    def details(self):
        """Creates a string detailing all modifiers and overrides of the current
        Ability instance

        Returns
        -------
        str
            Formatted for printing all information affecting current Ability

        """

        def tuple_convert(item: typing.Tuple):
            return "{} {}".format(*item)

        _perm = '\n\t'.join(map(tuple_convert, self._mod_permanent.items()))
        _temp = '\n\t'.join(map(tuple_convert, self._mod_temporary.items()))
        _over = '\n\t'.join(map(tuple_convert, self._mod_override.items()))
        return self._details_formatter.format(
            base=self._base_score,
            permanent=_perm,
            temporary=_temp,
            overrides=_over,
        )


class AbilityScores:
    """AbilityScores manages a full array of scores both default and custom

    Getting and setting of individual abilities is similar to dictionary
    element access with additional handling in place to enforce that only
    Ability instances exist within an AbilityScores instance.

    Examples
    --------
    >>> AbilityScores()['str']
    Ability class for strength

    >>> AbilityScores()['str'] = 15
    Sets strength ability to the result of Ability(15)

    >>> AbilityScores()['str'] = Ability(15, racial=2)
    Sets strength to newly created Ability object

    >>> AbilityScores()['str'] = {'score': 15, 'racial': 2}
    Sets strength to Ability(score=15, racial=2)

    """

    _def_scores = 'str', 'dex', 'con', 'int', 'wis', 'cha'
    _roller = Roller()
    standard_array = (15, 14, 13, 12, 10, 8)

    def __init__(self, **scores):
        """AbilityScores allows for flexible declaration of abilities

        Parameters
        ----------
        scores : Dict[str, int], optional
            Score names and values provided as keyword arguments
            Scores default to the normal 5e array of
            str, dex, con, int, wis, cha
            All, some, or none of these may be provided on initialization
        """
        _input = {name: 10 for name in self._def_scores}
        scores = {key.strip('_'): val for key, val in scores.items()}
        _input.update(scores)
        self._array = {name: Ability(value) for name, value in _input.items()}
        _log.info("Loaded %s as ability scores", ', '.join(self._array.keys()))

    @classmethod
    def roll_array(cls, method: str = '4d6d1', number: int = 6):
        """Generates an n numbered array of values for abilities

        Parameters
        ----------
        method : str, optional
            Defines the method by which a score is rolled
            Defaults to 4d6d1 (the 5e rolling default)
        number : int, optional
            Defines the number of abilities to roll
            Defaults to 6 (the number of regular 5e abilities)

        Returns
        -------
        List[int]
            list containing "number" integer ability scores

        """
        tmp_log_level = _roll_log.getEffectiveLevel()
        _changed_log = False
        if tmp_log_level < logging.WARNING:
            _roll_log.setLevel(logging.WARNING)
            _changed_log = True
        tmp = [cls._roller.roll(method) for _ in range(number)]
        if _changed_log:
            _roll_log.setLevel(tmp_log_level)
        return tmp

    def __str__(self):
        """Creates pretty string of AbilityScores

        Returns
        -------
        str
            Created in form "ability: value, ability: value, ..."

        """
        return '\n'.join(f"{key}: {val}" for key, val in self._array.items())

    def roll(self, ability: str, method: str = '1d20') -> int:
        """Rolls using the modifier of the selected ability

        Parameters
        ----------
        ability : str
            Name of the desired ability as stored in class instance
        method : str, optional
            Roll to which modifier should be added (default: 1d20)

        Returns
        -------
        int
            Value of roll

        """
        _ability = self._array.get(ability, Ability())
        return self._roller.roll(f"{method}{_ability.modifier:+}")

    def __getitem__(self, item: str) -> Ability:
        return self._array.get(item, Ability())

    def __setitem__(self, key: str, value: typing.Any) -> typing.NoReturn:
        if isinstance(value, Ability):
            self._array[key] = value
        elif isinstance(value, int):
            self._array[key] = Ability(value)
        elif isinstance(value, dict):
            self._array[key] = Ability(**value)
        else:
            raise AbilityError(str(value))

