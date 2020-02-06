from pydnd import dice_bag

debug_enabled = True


def test_imports():
    assert hasattr(dice_bag, 'logging')
    assert hasattr(dice_bag, 'random')
    assert hasattr(dice_bag, 're')
    assert hasattr(dice_bag, 'typing')


def test_logging():
    assert hasattr(dice_bag, '_log')
    global debug_enabled
    debug_enabled = dice_bag._log.isEnabledFor(dice_bag.logging.DEBUG)
    if debug_enabled:
        print()
        dice_bag._log.debug('Change level to INFO before merge')
    assert dice_bag._log.isEnabledFor(dice_bag.logging.INFO)
    assert dice_bag._log.isEnabledFor(dice_bag.logging.WARNING)


def test_roller_existence():
    assert hasattr(dice_bag, 'Roller')
    assert callable(dice_bag.Roller)
    try:
        sample_roller = dice_bag.Roller()
    except AttributeError:
        assert False, "Roller __init__ failed"
    assert isinstance(sample_roller, dice_bag.Roller)


def test_roller_init():
    sample_roller = dice_bag.Roller()
    assert hasattr(sample_roller, '_randint')
    assert dice_bag.random.randint == sample_roller._randint


def test_roller_roll():
    sample_roller = dice_bag.Roller()
    assert hasattr(sample_roller, 'roll')
    assert 1 <= sample_roller.roll('1d20') <= 20


def test_roller_parse_command():
    sample_roller = dice_bag.Roller()
    assert hasattr(sample_roller, '_parse_command')
    assert hasattr(sample_roller, 'previous_command')
    assert isinstance(sample_roller.previous_command, list)
    assert callable(sample_roller._parse_command)
    static_command = ('_static', '5')
    assert sample_roller._parse_command('5') == static_command
    roll_command = ('_gen_pool', (1, 20), 'comment', 'attack')
    assert sample_roller._parse_command('1d20[attack]') == roll_command
    negative_command = ('negative', 1, '_gen_pool', (1, 10))
    assert sample_roller._parse_command('-1d10') == negative_command
    keep_command = ('_gen_pool', (2, 20), 'keep', (1, True))
    assert sample_roller._parse_command('2d20k1') == keep_command
    lowest_command = ('_gen_pool', (2, 20), 'keep', (1, False))
    assert sample_roller._parse_command('2d20kl1') == lowest_command
    drop_command = ('_gen_pool', (4, 6), 'keep', (3, True))
    assert sample_roller._parse_command('4d6d1') == drop_command
    highest_command = ('_gen_pool', (4, 6), 'keep', (3, False))
    assert sample_roller._parse_command('4d6dh1') == highest_command
