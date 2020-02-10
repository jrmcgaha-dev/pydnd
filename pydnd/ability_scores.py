import typing


class _Ability:

    _default_score = 10

    def __init__(self, score: int = None, **permanent_modifiers):
        if score is None:
            score = self._default_score
        self._base_score = score
        self._mod_permanent = dict(**permanent_modifiers)
        self._mod_temporary = dict()
        self._mod_override = dict()

    def __call__(self) -> int:
        # TODO: Change to score property after creation of method
        return self._base_score + sum(self._mod_permanent.values())

    def add_permanent_modifier(self,
                               mods: typing.Dict = None,
                               **kwarg_mods) -> typing.NoReturn:
        if mods is not None:
            self._mod_permanent.update(mods)
        if kwarg_mods:
            self._mod_permanent.update(kwarg_mods)
