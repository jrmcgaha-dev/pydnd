import typing


class _Ability:

    _default_score = 10

    def __init__(self, score: int = None):
        if score is None:
            score = self._default_score
        self._base_score = score

    def __call__(self) -> int:
        # TODO: Change to score property after creation of method
        return self._base_score
