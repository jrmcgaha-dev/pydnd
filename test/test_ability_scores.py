from logging import DEBUG, INFO, WARNING

from pydnd import ability_scores
from pydnd import exceptions


debug_enabled = False


def test_imports():
    assert hasattr(ability_scores, 'defaultdict')
    assert hasattr(ability_scores, 'logging')
    assert hasattr(ability_scores, 'typing')
    assert hasattr(ability_scores, 'Roller')
    assert hasattr(ability_scores, '_roll_log')


def test_logger():
    assert hasattr(ability_scores, '_log')
    if ability_scores._log.isEnabledFor(DEBUG):
        global debug_enabled
        debug_enabled = True
    assert ability_scores._log.isEnabledFor(INFO)
    assert ability_scores._log.isEnabledFor(WARNING)


def test_ability():
    if debug_enabled:
        print()
    assert hasattr(ability_scores, 'Ability')
    assert callable(ability_scores.Ability)
    assert hasattr(ability_scores.Ability, '_default_score')
    assert ability_scores.Ability._default_score == 10
    sample_ability = ability_scores.Ability()
    assert hasattr(sample_ability, '_base_score')
    assert sample_ability._base_score == ability_scores.Ability._default_score
    assert sample_ability() == (10, 0)
    assert hasattr(sample_ability, '_mod_permanent')
    assert hasattr(sample_ability, '_mod_temporary')
    assert hasattr(sample_ability, '_mod_override')
    assert sample_ability._mod_permanent == dict()
    assert sample_ability._mod_temporary == dict()
    assert sample_ability._mod_override == dict()
    ability_with_mods = ability_scores.Ability(12, racial=2, magic=1)
    assert ability_with_mods() == (15, 2)
    assert ability_with_mods._base_score == 12
    assert 'racial' in ability_with_mods._mod_permanent.keys()
    assert 'magic' in ability_with_mods._mod_permanent.keys()
    assert ability_with_mods._mod_permanent.get('racial') == 2
    assert ability_with_mods._mod_permanent.get('magic') == 1


def test_ability_str():
    if debug_enabled:
        print()
    sample_ability = ability_scores.Ability()
    assert str(sample_ability) == '10 (+0)'
    sample_ability.add_permanent_modifier(racial=2)
    assert str(sample_ability) == '12 (+1)'
    sample_ability._mod_temporary['enhancement'].append(2)
    assert str(sample_ability) == '12+2<Temp>= 14 (+2)'
    sample_ability._mod_override['ogre'] = 19
    assert str(sample_ability) == '19<Override> (+4)'
    neg_ability = ability_scores.Ability(8)
    assert str(neg_ability) == '8 (-1)'


def test_ability_score():
    sample_ability = ability_scores.Ability()
    assert hasattr(sample_ability, 'score')
    assert sample_ability.score == 10
    perm_modded_ability = ability_scores.Ability(racial=2)
    assert perm_modded_ability.score == 12
    perm_modded_ability.score = 14
    assert perm_modded_ability.score == 14
    assert perm_modded_ability._base_score == 14
    assert perm_modded_ability._mod_permanent == dict()


def test_ability_modifier():
    sample_ability = ability_scores.Ability()
    assert hasattr(sample_ability, 'modifier')
    assert sample_ability.modifier == 0
    sample_ability.score = 8
    assert sample_ability.modifier == -1
    sample_ability.score = 12
    assert sample_ability.modifier == 1
    sample_ability.score = 1
    assert sample_ability.modifier == -5
    sample_ability.score = 15
    assert sample_ability.modifier == 2


def test_ability_temp_total():
    sample_ability = ability_scores.Ability()
    assert hasattr(sample_ability, '_temp_total')
    assert sample_ability._temp_total == 0
    sample_ability._mod_temporary['enhancement'].append(2)
    assert sample_ability._temp_total == 2
    sample_ability._mod_temporary['enhancement'].append(4)
    assert sample_ability._temp_total == 4
    sample_ability._mod_temporary['luck'].append(2)
    assert sample_ability._temp_total == 6


def test_ability_override():
    sample_ability = ability_scores.Ability()
    assert hasattr(sample_ability, '_override')
    assert sample_ability._override == -255
    sample_ability._mod_override['ogre'] = 19
    assert sample_ability._override == 19
    sample_ability._mod_override['cloud'] = 29
    assert sample_ability._override == 29


def test_ability_add_permanent_modifier():
    if debug_enabled:
        print()
    sample_ability = ability_scores.Ability()
    assert hasattr(sample_ability, 'add_permanent_modifier')
    sample_ability.add_permanent_modifier({'racial': 2})
    assert 'racial' in sample_ability._mod_permanent.keys()
    assert sample_ability() == (12, 1)
    sample_ability.add_permanent_modifier(magic=1)
    assert 'magic' in sample_ability._mod_permanent.keys()
    assert sample_ability() == (13, 1)


def test_ability_details():
    assert hasattr(ability_scores.Ability, '_details_formatter')
    sample_ability = ability_scores.Ability()
    expected = ability_scores.Ability._details_formatter.format(
        base=10,
        permanent='',
        temporary='',
        overrides='',
    )
    assert sample_ability.details == expected
    sample_ability.add_permanent_modifier(racial=2)
    sample_ability._mod_temporary['enhancement'].append(2)
    sample_ability._mod_override['ogre'] = 19
    expected = ability_scores.Ability._details_formatter.format(
        base=10,
        permanent='racial 2',
        temporary='enhancement [2]',
        overrides='ogre 19'
    )
    assert sample_ability.details == expected


def test_ability_scores_class():
    assert hasattr(ability_scores, 'AbilityScores')
    assert hasattr(ability_scores.AbilityScores, '_roller')
    assert hasattr(ability_scores.AbilityScores, '_def_scores')
    assert hasattr(ability_scores.AbilityScores, 'standard_array')
    sample_ability_scores = ability_scores.AbilityScores()
    assert hasattr(sample_ability_scores, '_array')
    assert isinstance(sample_ability_scores._array, dict)
    def_scores = ability_scores.AbilityScores._def_scores
    assert all(val in sample_ability_scores._array.keys() for val in def_scores)
    for val in sample_ability_scores._array.values():
        assert isinstance(val, ability_scores.Ability)
        assert val() == (10, 0)
    extended_scores = ability_scores.AbilityScores(sanity=12)
    assert 'sanity' in extended_scores._array.keys()
    sanity_value = extended_scores._array.get('sanity')
    assert isinstance(sanity_value, ability_scores.Ability)
    assert sanity_value() == (12, 1)


def test_ability_scores_roll_array():
    assert hasattr(ability_scores.AbilityScores, 'roll_array')
    sample_array = ability_scores.AbilityScores.roll_array()
    assert isinstance(sample_array, list)
    assert len(sample_array) == 6
    assert all(3 <= val <= 18 for val in sample_array)
    strange_array = ability_scores.AbilityScores.roll_array('10d6k3')
    assert len(strange_array) == 6
    assert all(3 <= val <= 18 for val in strange_array)
    extended_array = ability_scores.AbilityScores.roll_array(number=8)
    assert len(extended_array) == 8
    assert all(3 <= val <= 18 for val in extended_array)


def test_ability_scores_str():
    sample_array = ability_scores.AbilityScores()
    assert hasattr(sample_array, '__str__')
    expected = ("str: 10 (+0)\n"
                "dex: 10 (+0)\n"
                "con: 10 (+0)\n"
                "int: 10 (+0)\n"
                "wis: 10 (+0)\n"
                "cha: 10 (+0)")
    assert str(sample_array) == expected


def test_ability_scores_roll():
    sample_array = ability_scores.AbilityScores(str=15)
    assert hasattr(sample_array, 'roll')
    assert 1 <= sample_array.roll('int') <= 20
    assert 3 <= sample_array.roll('str') <= 22
    assert 1 <= sample_array.roll('int', '1d2') <= 2
    assert 3 <= sample_array.roll('str', '1d2') <= 4


def test_ability_score_get_set():
    sample_array = ability_scores.AbilityScores()
    assert hasattr(sample_array, '__getitem__')
    assert hasattr(sample_array, '__setitem__')
    assert isinstance(sample_array['str'], ability_scores.Ability)
    sample_array['str'] = ability_scores.Ability(12)
    assert sample_array['str'].score == 12
    sample_array['str'] = 14
    assert sample_array['str'].score == 14
    sample_array['str'] = {'score': 14, 'racial': 2}
    assert sample_array['str'].score == 16
    try:
        sample_array['str'] = 'Invalid'
    except exceptions.AbilityError:
        assert True
    assert sample_array['str'].score == 16
