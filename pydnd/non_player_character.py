import typing

from pydnd._character import _Character
from pydnd.monster import Monster
from pydnd.dice_bag import Roller


class NonPlayerCharacter(_Character, Monster):
    pass
