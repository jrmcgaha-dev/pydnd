"""
The dice_bag module is designed to handle parsing of roll commands
based upon a limited set of the commands available on roll20.net
"""
import logging
import random
import re
import typing


logging.basicConfig(level=logging.DEBUG)
# Remove above before merge
_log = logging.getLogger(__name__)
RANDINT_FUNCTION = typing.Callable[[int, int], int]


class Roller:
    def __init__(self, randint_function: RANDINT_FUNCTION = random.randint):
        self._randint = randint_function
