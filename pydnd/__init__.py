"""pydnd serves as a manager for various Dungeons and Dragons entities
with rolling and interaction integrated with storage and customization.
"""
import logging


logging.basicConfig(
    format='%(name)s [%(asctime)s] [%(levelname)s]: %(message)s',
    datefmt='%H:%M',
    level=logging.INFO,
)


from pydnd.ability_scores import Ability, AbilityScores
from pydnd.creature import Creature
from pydnd.monster import Monster
from pydnd.dice_bag import Roller


roll = Roller().roll
