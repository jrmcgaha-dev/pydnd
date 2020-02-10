"""
The dice_bag module is designed to handle parsing of roll commands
based upon a limited set of the commands available on "roll20.net"
"""
import logging
import random
import re
import typing


logging.basicConfig(level=logging.INFO)
_log = logging.getLogger(__name__)
RandIntFunction = typing.Callable[[int, int], int]
Action = typing.Union[int, str, type(re.match(".*", "type"))]
Resolution = typing.Union[int, str]


class Roller:
    """
    Roller class accepts  a random.randint style function upon
    initialization should the user decide that a specific degree
    of randomness is required for their dice rolls with the default
    randint sourced from python's built-in random module. Any provided
    function should mirror randint's functionality.
    """

    _action_pattern = (
        "(-)?(\\d+)d(\\d+)"
        "(?:r(?P<once>o)?(?P<reroll>\\d+))?"
        "(?:(?P<dk>[dk][hl]?)(?P<dk_num>\\d+))?"
    )
    _action_compiled = re.compile(_action_pattern)

    def __init__(self, randint_function: RandIntFunction = None):
        if randint_function is None:
            randint_function = random.randint
        self._randint = randint_function

    @classmethod
    def _parse_command(cls, command: str) -> typing.Tuple:
        _log.debug("command == %r", command)
        command = command + ' '
        _command, _message = command.split(' ', 1)
        _log.debug("_command == %r", _command)
        _log.debug("_message == %r", _message)
        _command = _command[0] + str.replace(_command[1:], '-', '+-')
        _log.debug("- to +-: _command == %r", _command)
        _actions = _command.split('+')
        _log.debug("_actions == %r", _actions)
        _parsed = (
            int(item)
            if re.fullmatch('\\d+', item)
            else cls._action_compiled.fullmatch(item)
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

    @staticmethod
    def _pool_dk(pool: typing.Tuple[int, ...],
                 mode: str,
                 num: int) -> typing.Tuple[int, ...]:
        _log.debug("Input: %r, %r, %r", pool, mode, num)
        if mode == 'd' or mode == 'dl':
            res = pool[num:]
        elif mode == 'dh':
            res = pool[:-num]
        elif mode == 'k' or mode == 'kh':
            res = pool[-num:]
        else:
            res = pool[:num]
        if not res:
            _log.debug('All dropped. Returning (0, 0)')
            return 0, 0
        return res

    def _resolve_action(self, action: Action) -> Resolution:
        if isinstance(action, (int, str)):
            _log.debug("Action `%r` requires no resolving", action)
            return action
        _num_dice = int(action.group(2))
        _num_sides = int(action.group(3))
        _reroll = int(action.group('reroll') or 0)
        _once = bool(action.group('once'))
        pool = self._dice_pool(_num_dice,
                               _num_sides,
                               _reroll,
                               _once)
        if action.group('dk'):
            _log.debug("pre-drop pool: %r", pool)
            results = self._pool_dk(pool,
                                    action.group('dk'),
                                    int(action.group('dk_num')))
        else:
            results = pool
        pretty_results = ', '.join(map(str, results))
        total = sum(results)
        if action.group(1):
            total *= -1
        _log.info(" %s : %s => %s",
                  action.group(0),
                  pretty_results,
                  total)
        return total

    def roll(self, input_: str) -> int:
        """
        The roll method handles actually performing a roll based upon
        a string input that is similar to the style used by "roll20.net".
        See the Notes section for further examples and details on syntax.

        ...

        Parameters
        ----------
        input_: str
            Full dice roll command as a single string

        Returns
        -------
        int
            Value of fully resolved command

        Notes
        -----

        1d20 : roll one 20 sided die
        2d20d1 : roll two 20 sided dice dropping the lowest one
        2d20k1 : roll two 20 sided dice keeping the highest one
        1d10r2 : roll one 10 sided die re-rolling any value <=2
        1d10ro2 : roll one 10 sided die re-rolling <=2 only once

        For re-rolling, a value is required
        2d10r will just roll two 10 sided dice normally
        2d10r1 will re-roll values of one as expected

        For re-rolling and keeping, order matters
        2d10d1r2 will fail to parse
        2d10r2d1 will work as expected (2d10 re-roll <=2 drop lowest 1)

        Operators
        Addition (+) and subtraction (-) are currently supported while
        multiplication (*), division (/), and exponentiation (**) are
        currently not functional.
        """
        _prep_input = self._parse_command(input_)
        _results = tuple(map(self._resolve_action, _prep_input))
        _total = sum(_results[:-1])
        if _results[-1]:
            _log.info(" Total: %s Message: %s", _total, _results[-1])
        else:
            _log.info(" Total: %s", _total)
        return _total
