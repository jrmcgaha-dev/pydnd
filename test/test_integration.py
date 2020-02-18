import pydnd


def test_rolling():
    assert 1 <= pydnd.roll('1d20') <= 20
    assert 5 <= pydnd.roll('1d20+4') <= 24


def test_custom_roller():
    import secrets

    def random_num(a: int, b: int) -> int:
        return secrets.choice(range(a, b+1))

    custom = pydnd.Roller(random_num)
    assert 1 <= custom.roll('1d20') <= 20
    assert 5 <= custom.roll('1d20+4') <= 24


def test_monster():
    goblin = pydnd.Monster()
    goblin.name = 'Bill'
    assert goblin.name == 'Bill'
    goblin.size = 'small'
    assert goblin.size == 'small'
    assert goblin.size_multiplier == 1
    goblin.type = 'humanoid (goblin)'
    assert goblin.type == 'humanoid (goblin)'
    goblin.attributes['str'] = 8
    goblin.attributes['dex'] = 14
    goblin.attributes['con'] = 10
    goblin.attributes['int'] = 10
    goblin.attributes['wis'] = 8
    goblin.attributes['cha'] = 8
    assert goblin.attributes['str']() == (8, -1)
    assert 0 <= goblin.attributes.roll('str') <= 19
    goblin.hit_dice_number = 2
    assert goblin.hit_dice_number == 2
    goblin.challenge_rating = 1/4
    assert goblin.avg_hp == 7
    assert goblin.proficiency == 2
    assert goblin.experience == 50
    goblin.add_language('Common')
    goblin.add_language('Goblin')
    assert goblin.languages == 'Common, Goblin'
    goblin.alignment = 'ne'
    assert goblin.alignment == 'Neutral Evil'
