from pydnd import exceptions


def test_root_exception():
    assert hasattr(exceptions, 'PydndException')
    assert Exception in exceptions.PydndException.__bases__
    try:
        raise exceptions.PydndException
    except exceptions.PydndException:
        assert True


def test_parsing_exception():
    assert hasattr(exceptions, 'ParseError')
    assert exceptions.PydndException in exceptions.ParseError.__bases__
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
