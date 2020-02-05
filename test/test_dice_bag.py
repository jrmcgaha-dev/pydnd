from pydnd import dice_bag

debug_enabled = True


def test_imports():
    assert hasattr(dice_bag, 'logging')
    assert hasattr(dice_bag, 'random')
    assert hasattr(dice_bag, 're')


def test_logging():
    assert hasattr(dice_bag, '_log')
    global debug_enabled
    debug_enabled = dice_bag._log.isEnabledFor(dice_bag.logging.DEBUG)
    if debug_enabled:
        print()
        dice_bag._log.debug('Change level to INFO before merge')
    assert dice_bag._log.isEnabledFor(dice_bag.logging.INFO)
    assert dice_bag._log.isEnabledFor(dice_bag.logging.WARNING)


def test_roll_d():
    if debug_enabled:
        print()
    assert hasattr(dice_bag, '_roll_d')
    assert callable(dice_bag._roll_d)
    assert dice_bag._roll_d(1) == 1
    assert 1 <= dice_bag._roll_d(10) <= 10
    assert 1 <= dice_bag._roll_d(1000) <= 1000
    assert dice_bag._roll_d(-1) == 0


def test_roll():
    if debug_enabled:
        print()
    assert hasattr(dice_bag, 'roll')
    assert 1 <= dice_bag.roll('1d20') <= 20
    assert 4 <= dice_bag.roll('1d20+3') <= 23
    assert 3 <= dice_bag.roll('3d6') <= 18
    complex_pattern = "1d20+5+1+2d6+15d4-2d10-30 + 2"
    assert -24 <= dice_bag.roll(complex_pattern) <= 68
    assert dice_bag.roll('apple') == 0


def test_dice_pool():
    if debug_enabled:
        print()
    assert hasattr(dice_bag, '_dice_pool')
    assert 1 <= dice_bag._dice_pool(1, 20) <= 20
    assert 2 <= dice_bag._dice_pool(2, 20) <= 40
    assert 5 <= dice_bag._dice_pool(5, 4) <= 20
