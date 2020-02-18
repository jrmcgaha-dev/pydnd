import argparse
import logging
import sys

from pydnd import dice_bag


logging.basicConfig(level=logging.DEBUG)
# Change above to INFO before merge
_log = logging.getLogger('pydnd')
roller = dice_bag.Roller()


def main(*_args):
    parser = argparse.ArgumentParser(prog="pydnd", description="Roll some dice")
    parser.add_argument('pos_rolls', nargs='*', type=str)
    parser.add_argument('-r', '--roll', nargs='*', type=str)
    parser.add_argument('-m', '--message', type=str, default='')
    if len(sys.argv) <= 1 and not _args:
        parser.print_help()
        exit()
    if _args:
        args = parser.parse_args(_args)
    else:
        args = parser.parse_args()
    if args.roll is None:
        args.roll = list()
    for _item in args.pos_rolls:
        roller.roll(_item)
    for _item in args.roll:
        roller.roll(_item)
    if args.message:
        _log.info("message: %s", args.message)


if __name__ == '__main__':
    main()
    exit()
