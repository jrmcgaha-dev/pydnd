from logging import DEBUG, INFO, WARNING

from pydnd import ability_scores


debug_enabled = False


def test_imports():
    assert hasattr(ability_scores, 'defaultdict')
    assert hasattr(ability_scores, 'logging')
    assert hasattr(ability_scores, 'typing')
    assert hasattr(ability_scores, 'Roller')


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
    assert hasattr(ability_scores, '_Ability')
    assert callable(ability_scores._Ability)
    assert hasattr(ability_scores._Ability, '_default_score')
    assert ability_scores._Ability._default_score == 10
    sample_ability = ability_scores._Ability()
    assert hasattr(sample_ability, '_base_score')
    assert sample_ability._base_score == ability_scores._Ability._default_score
    assert sample_ability() == (10, 0)
    assert hasattr(sample_ability, '_mod_permanent')
    assert hasattr(sample_ability, '_mod_temporary')
    assert hasattr(sample_ability, '_mod_override')
    assert sample_ability._mod_permanent == dict()
    assert sample_ability._mod_temporary == dict()
    assert sample_ability._mod_override == dict()
    ability_with_mods = ability_scores._Ability(12, racial=2, magic=1)
    assert ability_with_mods() == (15, 2)
    assert ability_with_mods._base_score == 12
    assert 'racial' in ability_with_mods._mod_permanent.keys()
    assert 'magic' in ability_with_mods._mod_permanent.keys()
    assert ability_with_mods._mod_permanent.get('racial') == 2
    assert ability_with_mods._mod_permanent.get('magic') == 1


def test_ability_str():
    if debug_enabled:
        print()
    sample_ability = ability_scores._Ability()
    assert str(sample_ability) == '10 (+0)'
    sample_ability.add_permanent_modifier(racial=2)
    assert str(sample_ability) == '12 (+1)'
    sample_ability._mod_temporary['enhancement'].append(2)
    assert str(sample_ability) == '12+2<Temp>= 14 (+2)'
    sample_ability._mod_override['ogre'] = 19
    assert str(sample_ability) == '19<Override> (+4)'
    neg_ability = ability_scores._Ability(8)
    assert str(neg_ability) == '8 (-1)'


def test_ability_score():
    sample_ability = ability_scores._Ability()
    assert hasattr(sample_ability, 'score')
    assert sample_ability.score == 10
    perm_modded_ability = ability_scores._Ability(racial=2)
    assert perm_modded_ability.score == 12
    perm_modded_ability.score = 14
    assert perm_modded_ability.score == 14
    assert perm_modded_ability._base_score == 14
    assert perm_modded_ability._mod_permanent == dict()


def test_ability_modifier():
    sample_ability = ability_scores._Ability()
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
    sample_ability = ability_scores._Ability()
    assert hasattr(sample_ability, '_temp_total')
    assert sample_ability._temp_total == 0
    sample_ability._mod_temporary['enhancement'].append(2)
    assert sample_ability._temp_total == 2
    sample_ability._mod_temporary['enhancement'].append(4)
    assert sample_ability._temp_total == 4
    sample_ability._mod_temporary['luck'].append(2)
    assert sample_ability._temp_total == 6


def test_ability_override():
    sample_ability = ability_scores._Ability()
    assert hasattr(sample_ability, '_override')
    assert sample_ability._override == -255
    sample_ability._mod_override['ogre'] = 19
    assert sample_ability._override == 19
    sample_ability._mod_override['cloud'] = 29
    assert sample_ability._override == 29


def test_ability_add_permanent_modifier():
    if debug_enabled:
        print()
    sample_ability = ability_scores._Ability()
    assert hasattr(sample_ability, 'add_permanent_modifier')
    sample_ability.add_permanent_modifier({'racial': 2})
    assert 'racial' in sample_ability._mod_permanent.keys()
    assert sample_ability() == (12, 1)
    sample_ability.add_permanent_modifier(magic=1)
    assert 'magic' in sample_ability._mod_permanent.keys()
    assert sample_ability() == (13, 1)


def test_ability_details():
    assert hasattr(ability_scores._Ability, '_details_formatter')
    sample_ability = ability_scores._Ability()
    expected = ability_scores._Ability._details_formatter.format(
        base=10,
        permanent='',
        temporary='',
        overrides='',
    )
    assert sample_ability.details == expected
    sample_ability.add_permanent_modifier(racial=2)
    sample_ability._mod_temporary['enhancement'].append(2)
    sample_ability._mod_override['ogre'] = 19
    expected = ability_scores._Ability._details_formatter.format(
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
    sample_ability_scores = ability_scores.AbilityScores()
    assert hasattr(sample_ability_scores, '_array')
    assert isinstance(sample_ability_scores._array, dict)
    def_scores = ability_scores.AbilityScores._def_scores
    assert all(val in sample_ability_scores._array.keys() for val in def_scores)
    for val in sample_ability_scores._array.values():
        assert isinstance(val, ability_scores._Ability)
        assert val() == (10, 0)
    extended_scores = ability_scores.AbilityScores(sanity=12)
    assert 'sanity' in extended_scores._array.keys()
    sanity_value = extended_scores._array.get('sanity')
    assert isinstance(sanity_value, ability_scores._Ability)
    assert sanity_value() == (12, 1)
