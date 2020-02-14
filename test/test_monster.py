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
    assert hasattr(monster.Monster, '_size_mult_to_hp')
    sample_monster = monster.Monster()
    assert hasattr(sample_monster, 'alignment')
    assert hasattr(sample_monster, 'challenge_rating')
    assert hasattr(sample_monster, 'hit_dice_number')


def test_monster_challenge_to_experience():
    assert isinstance(monster.Monster._challenge_to_experience, dict)
    cr2xp = monster.Monster._challenge_to_experience
    table_keys = map(str, range(1, 31))
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


def test_monster_proficiency():
    sample_monster = monster.Monster()
    assert hasattr(sample_monster, 'proficiency')
    assert sample_monster.proficiency == 2
    sample_monster.challenge_rating = 7
    assert sample_monster.proficiency == 3
    sample_monster.challenge_rating = 28
    assert sample_monster.proficiency == 8
    sample_monster.challenge_rating = 32.5
    assert sample_monster.proficiency == 9


def test_monster_avg_hp():
    sample_monster = monster.Monster()
    assert hasattr(sample_monster, 'avg_hp')
    assert sample_monster.avg_hp == 4
    sample_monster.hit_dice_number = 2
    assert sample_monster.avg_hp == 9
    sample_monster.attributes = monster.AbilityScores(con=12)
    assert sample_monster.avg_hp == 11
    sample_monster.size = 'huge'
    assert sample_monster.avg_hp == 15
