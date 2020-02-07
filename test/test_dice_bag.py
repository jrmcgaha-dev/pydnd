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
    assert hasattr(dice_bag.Roller, '_action_pattern')
    assert hasattr(dice_bag.Roller, '_action_compiled')
    assert hasattr(dice_bag.Roller, '_parse_command')
    assert callable(dice_bag.Roller._parse_command)
    static_test = '5+3'
    static_result = (5, 3, '')
    assert dice_bag.Roller._parse_command(static_test) == static_result
    dice_test = '1d20'
    dice_result = dice_bag.Roller._action_compiled.fullmatch(dice_test)
    _experiment = dice_bag.Roller._parse_command(dice_test)
    assert dice_result.groups() == _experiment[0].groups()


def test_resolve_action():
    sample_roller = dice_bag.Roller()
    assert hasattr(sample_roller, '_resolve_action')
    assert callable(sample_roller._resolve_action)
    assert 1 <= sample_roller._resolve_action('1d20') <= 20
    assert sample_roller._resolve_action(5) == 5
    assert sample_roller._resolve_action('Message') == 'Message'
    assert 3 <= sample_roller._resolve_action('1d8r2') <= 8
    assert 1 <= sample_roller._resolve_action('1d8ro2') <= 8
    assert 3 <= sample_roller._resolve_action('4d6d1') <= 18
    assert 1 <= sample_roller._resolve_action('4d6k1') <= 6
    assert 2 <= sample_roller._resolve_action('4d6r1k1') <= 6


def test_dice_pool():
    sample_roller = dice_bag.Roller()
    assert hasattr(sample_roller, '_dice_pool')
    assert callable(sample_roller._dice_pool)
    single_pool = sample_roller._dice_pool(1, 20)
    assert isinstance(single_pool, list)
    assert single_pool
    assert isinstance(single_pool[0], int)
    assert 1 <= single_pool[0] <= 20
    many_reroll = sample_roller._dice_pool(2, 10, 1)
    assert many_reroll
    assert all(2 <= item <= 10 for item in many_reroll)
    single_reroll = sample_roller._dice_pool(2, 10, 2, True)
    assert single_reroll
    assert all(1 <= item <= 10 for item in single_reroll)
