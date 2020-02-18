"""pydnd serves as a manager for various Dungeons and Dragons entities
with rolling and interaction integrated with storage and customization.
"""
import logging


logging.basicConfig(
    format='%(name)s.%(module)s [%(asctime)s] [%(levelname)s]: %(message)s',
    datefmt='%H:%M',
    level=logging.INFO,
)


from pydnd import ability_scores, creature, monster
from pydnd.dice_bag import Roller


roll = Roller().roll
