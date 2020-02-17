from pydnd import __main__


def test_imports():
    assert hasattr(__main__, 'argparse')
    assert hasattr(__main__, 'logging')
    assert hasattr(__main__, 'sys')
    assert hasattr(__main__, 'dice_bag')


def test_main():
    assert hasattr(__main__, 'main')
    assert callable(__main__.main)
