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
