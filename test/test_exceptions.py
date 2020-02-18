from pydnd import exceptions


def test_root_exception():
    assert hasattr(exceptions, 'PydndException')
    assert Exception in exceptions.PydndException.__bases__
    try:
        raise exceptions.PydndException
    except exceptions.PydndException:
        assert True
