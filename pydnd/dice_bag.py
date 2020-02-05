import logging
import random
import re


logging.basicConfig(level=logging.DEBUG)
# Remove above before merge
_log = logging.getLogger(__name__)


def _roll_d(m_val: int) -> int:
    _log.debug("m_val == %r", m_val)
    if not isinstance(m_val, int):
        _log.warning("_roll_val only accepts int values")
        return 0
    if m_val < 1:
        _log.warning("_roll_val only accepts values >= 1")
        return 0
    _log.debug("returning random.randint(1, %r)", m_val)
    return random.randint(1, m_val)


def _dice_pool(num: int, val: int) -> int:
    _log.debug("input: num = %r, val = %r", num, val)
    _num = abs(num)
    _res = sorted([_roll_d(val) for _ in range(_num)])
    _log.debug('set res = %r', _res)
    _log.info("%sd%s: %s", _num, val, ', '.join(map(str, _res)))
    _sign = num // _num
    return _sign * sum(_res)


_dice_pattern = r"([\+\-]\d+)d(\d+)"
_static_pattern = r"[\+\-]\d+(?=[\+\-])"


def roll(dice: str) -> int:
    par = dice.lower().replace(' ', '')
    # normalize the input
    _log.debug("set par = %r", par)
    if par[0] not in '+-':
        par = '+' + par
        _log.debug("change par to %r", par)
        # tweak input to play nice with re.findall and our pattern
    par += '+0'
    _log.debug("change par to %r", par)
    # one last tweak for helping the pattern
    _dice = re.findall(_dice_pattern, par)
    _log.debug("set _dice = %r", _dice)
    _static = re.findall(_static_pattern, par)
    _log.debug("set _static = %r", _static)
    if not (_dice and _static):
        _log.warning("Failed to parse input %r", dice)
        return 0
