from collections import defaultdict
import logging
import typing


logging.basicConfig(level=logging.DEBUG)
# Change above to INFO before merge
_log = logging.getLogger(__name__)


class _Ability:

    _default_score = 10

    def __init__(self, score: int = None, **permanent_modifiers):
        if score is None:
            score = self._default_score
        self._base_score = score
        _log.debug("set _base_score = %r", self._base_score)
        self._mod_permanent = dict(**permanent_modifiers)
        _log.debug("set _mod_permanent = %r", self._mod_permanent)
        self._mod_temporary = defaultdict(list)
        self._mod_override = defaultdict(list)

    def __call__(self) -> int:
        # TODO: Change to score property after creation of method
        return self._base_score + sum(self._mod_permanent.values())

    def __str__(self) -> str:
        _core = self._base_score + sum(self._mod_permanent.values())
        return str(_core)

    def add_permanent_modifier(self,
                               mods: typing.Dict = None,
                               **kwarg_mods) -> typing.NoReturn:
        _log.debug("Before addition: %r", self._mod_permanent)
        if mods is not None:
            self._mod_permanent.update(mods)
        if kwarg_mods:
            self._mod_permanent.update(kwarg_mods)
        _log.debug("After addition: %r", self._mod_permanent)

    def add_temporary_modifier(self,
                               mods: typing.Dict = None,
                               **kwarg_mods) -> typing.NoReturn:
        _log.debug("Before addition: %r", self._mod_temporary)
        if mods is not None:
            for _key, _val in mods.items():
                self._mod_temporary[_key].append(_val)
        for _key, _val in kwarg_mods.items():
            self._mod_temporary[_key].append(_val)
