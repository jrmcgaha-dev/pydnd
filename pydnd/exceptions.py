class PydndException(Exception):
    """Base exception class for pydnd"""
    pass


class ParseError(PydndException):
    """Raised when an input value fails to parse correctly"""
    pass


class AbilityError(PydndException):
    """Raised when an input value is not an Ability or cannot be converted
    to an Ability"""
    pass
