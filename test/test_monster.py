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


def test_monster_challenge_to_experience():
    assert isinstance(monster.Monster._challenge_to_experience, dict)
    cr2xp = monster.Monster._challenge_to_experience
    table_keys = map(str, map(float, (1/8, 1/4, 1/2, *range(31))))
    assert all(key in cr2xp.keys() for key in table_keys)
    assert all(isinstance(value, int) for value in cr2xp.values())


def test_monster_experience():
    sample_monster = monster.Monster()
    assert hasattr(sample_monster, 'experience')
    assert sample_monster.experience == 0
    sample_monster.challenge_rating = 0.5
    assert sample_monster.experience == 100
    sample_monster.challenge_rating = 5
    assert sample_monster.experience == 1800
    sample_monster.challenge_rating = 5.5
    assert sample_monster.experience == 2050
    sample_monster.challenge_rating = 31
    assert sample_monster.experience == 155000+3100
    sample_monster.challenge_rating = 31.5
    assert sample_monster.experience == 155000+3100+1600
