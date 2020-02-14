from pydnd import monster


def test_imports():
    assert hasattr(monster, 'json')
    assert hasattr(monster, 'resource_stream')
    assert hasattr(monster, 'typing')
    assert hasattr(monster, 'AbilityScores')
    assert hasattr(monster, 'Creature')
    assert hasattr(monster, 'Roller')


def test_monster():
    assert hasattr(monster, 'Monster')
    assert callable(monster.Monster)
    assert monster.Creature in monster.Monster.__bases__
    assert hasattr(monster.Monster, '_challenge_to_experience')
    sample_monster = monster.Monster()
    assert hasattr(sample_monster, 'alignment')
    assert hasattr(sample_monster, 'challenge_rating')
