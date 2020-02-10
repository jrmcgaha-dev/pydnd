from pydnd import ability_scores


def test_imports():
    assert hasattr(ability_scores, 'typing')


def test_ability():
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
