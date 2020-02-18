from pydnd import scripts


def test_imports():
    assert hasattr(scripts, 'argparse')
    assert hasattr(scripts, 'logging')
    assert hasattr(scripts, 'sys')
    assert hasattr(scripts, 'dice_bag')


def test_main():
    assert hasattr(scripts, 'main')
    assert callable(scripts.main)
