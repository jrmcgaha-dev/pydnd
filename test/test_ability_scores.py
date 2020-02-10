from logging import DEBUG, INFO, WARNING

from pydnd import ability_scores


debug_enabled = False


def test_imports():
    assert hasattr(ability_scores, 'defaultdict')
    assert hasattr(ability_scores, 'logging')
    assert hasattr(ability_scores, 'typing')


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
    assert sample_ability() == 10
    assert hasattr(sample_ability, '_mod_permanent')
    assert hasattr(sample_ability, '_mod_temporary')
    assert hasattr(sample_ability, '_mod_override')
    assert sample_ability._mod_permanent == dict()
    assert sample_ability._mod_temporary == dict()
    assert sample_ability._mod_override == dict()
    ability_with_mods = ability_scores._Ability(12, racial=2, magic=1)
    assert ability_with_mods() == 15
    assert ability_with_mods._base_score == 12
    assert 'racial' in ability_with_mods._mod_permanent.keys()
    assert 'magic' in ability_with_mods._mod_permanent.keys()
    assert ability_with_mods._mod_permanent.get('racial') == 2
    assert ability_with_mods._mod_permanent.get('magic') == 1


def test_ability_str():
    if debug_enabled:
        print()
    sample_ability = ability_scores._Ability()
    assert str(sample_ability) == '10'
    sample_ability.add_permanent_modifier(racial=2)
    assert str(sample_ability) == '12'


def test_add_permanent_modifier():
    if debug_enabled:
        print()
    sample_ability = ability_scores._Ability()
    assert hasattr(sample_ability, 'add_permanent_modifier')
    sample_ability.add_permanent_modifier({'racial': 2})
    assert 'racial' in sample_ability._mod_permanent.keys()
    assert sample_ability() == 12
    sample_ability.add_permanent_modifier(magic=1)
    assert 'magic' in sample_ability._mod_permanent.keys()
    assert sample_ability() == 13


def test_add_temporary_modifier():
    if debug_enabled:
        print()
    sample_ability = ability_scores._Ability()
    assert hasattr(sample_ability, 'add_temporary_modifier')
    sample_ability.add_temporary_modifier({'enhancement': 4})
    assert sample_ability() == 14
    sample_ability.add_temporary_modifier(enhancement=2)
    assert sample_ability() == 14
    sample_ability._mod_temporary.get('enhancement').remove(4)
    assert sample_ability() == 12
