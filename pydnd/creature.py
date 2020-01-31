import logging
import re
import typing


logging.basicConfig(level=logging.DEBUG)
# TODO: Remove above before develop merge
_log: logging.Logger = logging.getLogger(__name__)
_log.debug("Establish that logger is active")


class Creature:

    _base_ac: int = 10
    _alignment_hash: typing.Dict[str, int] = {
        'l': 0,
        'g': 0,
        'n': 1,
        'c': 2,
        'e': 2,
        'u': 255,
    }
    _alignment_convert: typing.Dict[str, str] = {
        'l': 'Lawful',
        'g': 'Good',
        'n': 'Neutral',
        'e': 'Evil',
        'c': 'Chaotic'
    }

    def __init__(self):
        self.name: str = ''
        self.size: str = ''
        self.type: str = ''
        self._alignment: typing.Tuple[str, str] = ('', '')
        self.armor_class: int = 10
        self.hitpoints: int = 0
        self.speed: int = 0
        self.attributes: typing.Any = None
        # Attributes will eventually have custom handler class
        self.saving_throws: typing.List[str] = list()
        self.skills: typing.List[str] = list()
        self.damage_resistances: typing.List[str] = list()
        self.damage_vulnerabilities: typing.List[str] = list()
        self.damage_immunities: typing.List[str] = list()
        self.senses: typing.List[str] = list()
        self.languages: typing.List[str] = list()

    @property
    def alignment(self):
        """
        Get or set alignment for creature. Setting is read in
        law/chaos good/evil order (i.e. lawful good or lg would
        work but good lawful would not)

        Returns
        -------
        str
            Formatted string representing alignment

        """
        if self._alignment == ('', ''):
            return 'Unaligned'
        if self._alignment[0] == 'u':
            return 'Unaligned'
        _order_axis = self._alignment_convert.get(self._alignment[0])
        _moral_axis = self._alignment_convert.get(self._alignment[1])
        return ' '.join((_order_axis, _moral_axis)).title()

    @alignment.setter
    def alignment(self, value: str):
        par = value.lower().strip(' ')
        if par == 'u' or par == 'unaligned' or not par:
            self._alignment = ('u', '')
        else:
            _re_pattern = (
                "(lawful|neutral|chaotic|true|[clnt])?"
                "\\s?"
                "(good|neutral|evil|[gne])?"
            )
            par = re.match(_re_pattern, par)
            if par.group(0):
                _order = par.group(1) or 'n'
                _morality = par.group(2) or 'n'
                _order = _order[0].replace('t', 'n')
                _morality = _morality[0]
                self._alignment = (_order, _morality)
            else:
                _log.warning('Invalid data. Ignoring %s', value)

    @property
    def _alignment_coord(self):
        _order_coord = self._alignment_hash.get(self._alignment[0], 255)
        _morality_coord = self._alignment_hash.get(self._alignment[1], 255)
        return _order_coord, _morality_coord
