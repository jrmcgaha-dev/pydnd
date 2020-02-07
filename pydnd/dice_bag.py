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
        _log.debug("command == %r", command)
        command = command + ' '
        _command, _message = command.split(' ', 1)
        _log.debug("_command == %r", _command)
        _log.debug("_message == %r", _message)
        _command = str.replace(_command, '-', '+-')
        _log.debug("- to +-: _command == %r", _command)
        _actions = _command.split('+')
        _log.debug("_actions == %r", _actions)
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
        _log.debug("Input: %r, %r, %r, %r", num_dice, sides, reroll, once)
        lowest = min(1 if once else reroll+1, sides)
        _log.debug("lowest == %r", lowest)
        _pool = [self._randint(lowest, sides) for _ in range(num_dice)]
        _pool.sort()
        if not once:
            return tuple(_pool)
        _log.debug("Before reroll once: _pool == %r", _pool)
        for ind, val in enumerate(_pool):
            if val > reroll:
                break
            _pool[ind] = self._randint(lowest, sides)
        _log.debug("After reroll once and no sort: _pool == %r", _pool)
        _pool.sort()
        return tuple(_pool)
