from pydnd import __main__


def test_imports():
    assert hasattr(__main__, 'argparse')
    assert hasattr(__main__, 'logging')
    assert hasattr(__main__, 'dice_bag')
