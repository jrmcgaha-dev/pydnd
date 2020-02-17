import typing

from pydnd._character import _Character
from pydnd.dice_bag import Roller


class Player(_Character):
    """Player is a sub-class of _Character which itself is a sub-class of
    Creature. Players create characters that follow the standard rules of
    Dungeons and Dragons. This class handles managing the properties that
    are unique to players and masks tools that are better left for the
    Dungeon Master's use.

    Notes
    -----
    This class currently has no unique properties and serves as a placeholder
    for the intended structure of later developments in pydnd.

    """
    pass
