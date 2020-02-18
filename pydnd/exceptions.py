class PydndError(Exception):
    """Base exception class for pydnd"""
    pass


class ParseError(PydndError):
    """Raised when an input value fails to parse correctly"""
    pass


class AbilityError(PydndError):
    """Raised when an input value is not an Ability or cannot be converted
    to an Ability"""
    pass


class RollerError(PydndError):
    """Raised when Roller is given an improper function on initialization"""
    pass
