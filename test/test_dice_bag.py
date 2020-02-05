from pydnd import dice_bag


def test_imports():
    assert hasattr(dice_bag, 'logging')
    assert hasattr(dice_bag, 'random')
    assert hasattr(dice_bag, 're')


def test_roll_d():
    assert hasattr(dice_bag, '_roll_d')
    assert callable(dice_bag._roll_d)
    assert dice_bag._roll_d(1) == 1
    assert 1 <= dice_bag._roll_d(10) <= 10
    assert 1 <= dice_bag._roll_d(1000) <= 1000
