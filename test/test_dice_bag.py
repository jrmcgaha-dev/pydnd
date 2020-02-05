from pydnd import dice_bag


def test_imports():
    assert hasattr(dice_bag, 'random')
