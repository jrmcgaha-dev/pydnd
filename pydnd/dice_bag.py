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

    _action_pattern = (
        "(\\d+)d(\\d+)"
        "(r(?P<once>o)?(?P<reroll>\\d+))?"
        "((?P<dk>[dk][hl]?)(?P<dk_num>\\d+))?"
    )
    _action_compiled = re.compile(_action_pattern)

    def __init__(self, randint_function: RANDINT_FUNCTION = random.randint):
        self._randint = randint_function

    @staticmethod
    def _parse_command(command: str) -> typing.Tuple:
        command = command + ' '
        _command, _message = command.split(' ', 1)
        _command = str.replace(_command, '-', '+-')
        _actions = _command.split('+')
        _parsed = (
            int(item)
            if re.fullmatch('\\d+', item)
            else Roller._action_compiled.fullmatch(item)
            for item in _actions
        )
        return tuple(_parsed) + (_message,)

    def _dice_pool(self,
                   num_dice: int,
                   sides: int,
                   reroll: int = 0,
                   once: bool = False) -> typing.Tuple[int, ...]:
        lowest = min(1 if once else reroll+1, sides)
        _pool = [self._randint(lowest, sides) for _ in range(num_dice)]
        _pool.sort()
        if not once:
            return tuple(_pool)
        for ind, val in enumerate(_pool):
            if val > reroll:
                break
            _pool[ind] = self._randint(lowest, sides)
        _pool.sort()
        return tuple(_pool)
