from pydnd import creature


def test_imports():
    assert 'typing' in creature.__dict__


def test_class_existence():
    assert callable(creature.Creature)


def test_class_attribute_existence():
    assert hasattr(creature.Creature, '_default_ac')
    assert hasattr(creature.Creature, '_alignment_hash')


def test_class_instance_attribute_existence():
    empty_creature = creature.Creature()
    assert hasattr(empty_creature, 'name')
    assert hasattr(empty_creature, 'size')
    assert hasattr(empty_creature, 'type')
    assert hasattr(empty_creature, 'alignment')
    assert hasattr(empty_creature, 'armor_class')
    assert hasattr(empty_creature, 'hitpoints')
    assert hasattr(empty_creature, 'speed')
    assert hasattr(empty_creature, 'attributes')
    assert hasattr(empty_creature, 'saving_throws')
    assert hasattr(empty_creature, 'skills')
    assert hasattr(empty_creature, 'damage_resistances')
    assert hasattr(empty_creature, 'damage_vulnerabilities')
    assert hasattr(empty_creature, 'damage_immunities')
    assert hasattr(empty_creature, 'senses')
    assert hasattr(empty_creature, 'languages')


def test_class_instance_property_alignment_coord():
    empty_creature = creature.Creature()
    assert hasattr(empty_creature, '_alignment_coord')
    empty_creature.alignment = 'lg'
    assert empty_creature._alignment_coord == (0, 0)
    empty_creature.alignment = 'ce'
    assert empty_creature._alignment_coord == (2, 2)
    empty_creature.alignment = 'nn'
    assert empty_creature._alignment_coord == (1, 1)
    empty_creature.alignment = 'tn'
    assert empty_creature._alignment_coord == (1, 1)
    empty_creature.alignment = 'lawful good'
    assert empty_creature._alignment_coord == (0, 0)
    empty_creature.alignment = 'chaotic evil'
    assert empty_creature._alignment_coord == (2, 2)
    empty_creature.alignment = 'neutral neutral'
    assert empty_creature._alignment_coord == (1, 1)
    empty_creature.alignment = 'true neutral'
    assert empty_creature._alignment_coord == (1, 1)
