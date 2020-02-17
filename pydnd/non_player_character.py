import typing

from pydnd._character import _Character
from pydnd.monster import Monster
from pydnd.dice_bag import Roller


class NonPlayerCharacter(_Character, Monster):
    """NonPlayerCharacter is a sub-class of _Character and then Monster.
    Non-player characters (or NPC's) are characters built by the Dungeon
    Master and thus require the tools of both characters and monsters to
    properly encapsulate all of their potential features.

    Notes
    -----
    This class currently has no unique properties and serves as a placeholder
    for the intended structure of later developments in pydnd.

    """
    pass
