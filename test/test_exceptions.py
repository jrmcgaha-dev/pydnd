from pydnd import exceptions


def test_root_error():
    assert hasattr(exceptions, 'PydndError')
    assert Exception in exceptions.PydndError.__bases__
    try:
        raise exceptions.PydndError
    except exceptions.PydndError:
        assert True


def test_parsing_exception():
    assert hasattr(exceptions, 'ParseError')
    assert exceptions.PydndError in exceptions.ParseError.__bases__
    try:
        raise exceptions.ParseError
    except exceptions.ParseError:
        assert True


def test_ability_error():
    assert hasattr(exceptions, 'AbilityError')
    try:
        raise exceptions.AbilityError
    except exceptions.AbilityError:
        assert True


def test_roller_error():
    assert hasattr(exceptions, 'RollerError')
    try:
        raise exceptions.RollerError
    except exceptions.RollerError:
        assert True
