class PydndException(Exception):
    """Base exception class for pydnd"""
    pass


class ParseError(PydndException):
    """Raised when an input value fails to parse correctly"""
    pass
