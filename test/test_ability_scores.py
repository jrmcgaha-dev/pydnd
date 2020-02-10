from pydnd import ability_scores


def test_imports():
    assert hasattr(ability_scores, 'typing')


def test_ability():
    assert hasattr(ability_scores, '_Ability')
    assert callable(ability_scores._Ability)
    assert hasattr(ability_scores._Ability, '_default_score')
    assert ability_scores._Ability._default_score == 10
    sample_ability = ability_scores._Ability()
    assert sample_ability() == 10
