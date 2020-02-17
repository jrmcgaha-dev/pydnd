from pydnd import _main


def test_imports():
    assert hasattr(_main, 'argparse')
    assert hasattr(_main, 'logging')
    assert hasattr(_main, 'sys')
    assert hasattr(_main, 'dice_bag')


def test_main():
    assert hasattr(_main, 'main')
    assert callable(_main.main)
