# pydnd v0.1
Flexible Dungeons and Dragons entity manager and helper
# Installation
pydnd is structured to be installed via pip. It requires python 3.8 or later,
so check your python version before attempting to install by doing

`python --version`

to make sure that your version of python is compatible. If it is, installation
can be completed by navigating to where the outermost pydnd folder is (if you
can see setup.py, you have gone too far) and running

`python -m pip install pydnd`

to install the package to your python environment. If you want to use the
scripts included with pydnd, make sure that your environment path has the
scripts folder of your preferred python environment.
# Usage
### Rolling Dice
The most common action in Dungeons and Dragons is rolling dice, so this feature
is exposed at the outermost level, so it can be done a few different ways.
The first step is knowing the basic syntax for the dice.
#### Rolling Syntax
`xdy` - Roll _x_ number of _y_ sided dice

`xdydz` - Roll _x_ number of _y_ sided dice dropping the lowest _z_ dice

`xdykz` - Roll _x_ number of _y_ sided dice keeping the highest _z_ dice

_d_ is shorthand for _dl_ which stands for _drop lowest_

_k_ is shorthand for _kh_ which stands for _keep highest_

_dh_ and _kl_ (_drop highest_ and _keep lowest_ respectively) are also supported

`xdyrz` - Roll _x_ number of _y_ sided dice rerolling all values < = _z_

`xdyroz` - Roll _x_ number of _y_ sided dice rerolling < = _z_ only once
#### Calling Options
With python: `python -m pydnd 1d20`

With script: `pydnd 1d20`

In the interpreter with the package: 

```python
import pydnd
pydnd.roll('1d20')
```

In the interpreter with a custom randomizer:

```python
from custom_random_package import some_randint_function
from pydnd import dice_bag

roller = dice_bag.Roller(some_randint_function)
roller.roll('1d20')
```

### Managing Monsters
The Monster class in pydnd is designed to make creating creatures as painless
as possible. Many of the table lookups and calculations are built into the
class, so you have to input as little information as possible to get a monster
working. Much of a monster's math is based upon its size and cr, so once those
are entered, the rest of the setup is just telling the class what
proficiencies that creature has.

See `help(pydnd.Monster)` for more details.

### Making NPC's
The NonPlayerCharacter class is a work in progress. Please check back
regularly for any updates.

### Making a Character
The Player class is a work in progress. Please check back regularly for any
updates.

