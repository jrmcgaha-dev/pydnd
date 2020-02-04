import logging
import re
import typing


logging.basicConfig(level=logging.DEBUG)
# TODO: Remove above before develop merge
_log: logging.Logger = logging.getLogger(__name__)
_log.debug("Establish that logger is active")
_log.debug("Change logging level to INFO before develop merge")


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
    _size_hash: typing.Dict[str, int] = {
        'tiny': -1,
        'small': 0,
        'medium': 0,
        'large': 1,
        'huge': 2,
        'gargantuan': 3,
    }

    def __init__(self):
        self.name: str = ''
        self.size: str = ''
        self.type: str = ''
        self._alignment: typing.Tuple[str, str] = ('', '')
        self.armor_class: int = Creature._base_ac
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
        self._lang_list: typing.List[str] = list()

    @property
    def alignment(self) -> str:
        """
        Get or set alignment for creature. Setting is read in
        law/chaos good/evil order (i.e. lawful good or lg would
        work but good lawful would not)

        Returns
        -------
        str
            Formatted string representing alignment

        """
        _log.debug('Entering alignment getter')
        _log.debug('_alignment = %r', self._alignment)
        if self._alignment == ('', ''):
            return 'Unaligned'
        if self._alignment[0] == 'u':
            return 'Unaligned'
        _order_axis = self._alignment_convert.get(self._alignment[0])
        _moral_axis = self._alignment_convert.get(self._alignment[1])
        return ' '.join((_order_axis, _moral_axis)).title()

    @alignment.setter
    def alignment(self, value: str) -> typing.NoReturn:
        _log.debug('Entering alignment setter')
        _log.debug('value = %r', value)
        par = value.lower().strip(' ')
        _log.debug('set par = %r', par)
        if par == 'u' or par == 'unaligned' or not par:
            self._alignment = ('u', '')
        else:
            _re_pattern = (
                "(lawful|neutral|chaotic|true|[clnt])?"
                "\\s?"
                "(good|neutral|evil|[gne])?"
            )
            par = re.match(_re_pattern, par)
            _log.debug('set par = %r', par)
            _log.debug('par.group(0) = %r', par.group(0))
            _log.debug('par.group(1) = %r', par.group(1))
            _log.debug('par.group(2) = %r', par.group(2))
            if par.group(0):
                _order = par.group(1) or 'n'
                _morality = par.group(2) or 'n'
                _order = _order[0].replace('t', 'n')
                _morality = _morality[0]
                self._alignment = (_order, _morality)
                _log.debug('set self._alignment = %r', self._alignment)
            else:
                _log.warning('Invalid data. Ignoring %r', value)
        _log.debug('Exiting alignment setter')

    @property
    def _alignment_coord(self) -> typing.Tuple[int, int]:
        _order_coord = self._alignment_hash.get(self._alignment[0], 255)
        _morality_coord = self._alignment_hash.get(self._alignment[1], 255)
        return _order_coord, _morality_coord

    @property
    def size_multiplier(self) -> int:
        _log.debug("Entering size_multiplier")
        if not self.size:
            return 1
        par = self.size.lower().strip(' ')
        _log.debug("Stripped size: %r", par)
        _normal_sizes_pattern = '|'.join(self._size_hash.keys())
        _pattern = f"({_normal_sizes_pattern})(\\+*)"
        _log.debug("Pattern used: %r", _pattern)
        par = re.match(_pattern, par)
        if par is None or not par.group(0):
            _log.warning("Unable to parse size %r. Defaulting to 1", self.size)
            return 1
        _log.debug("Group 0: %r", par.group(0))
        _log.debug("Group 1: %r", par.group(1))
        _log.debug("Group 2: %r", par.group(2))
        _base_size = self._size_hash.get(par.group(1), 0)
        return pow(2, _base_size+len(par.group(2)))

    @property
    def languages(self):
        if not self._lang_list:
            _log.debug("bool(_lang_list) == False")
            return ''
        _log.debug("self._lang_list == %r", self._lang_list)
        return ', '.join(map(str.title, self._lang_list))

    def add_language(self, lang: str) -> str:
        par = lang.lower().strip(' ')
        _log.debug("set par = %r", par)
        self._lang_list.append(par)
        _log.debug("self._lang_list == %r", self._lang_list)
        return self.languages

    def remove_language(self, lang: str) -> str:
        par = lang.lower().strip(' ')
        _log.debug("set par = %r", par)
        if par in self._lang_list:
            self._lang_list.remove(par)
            _log.debug("par found and removed")
        return self.languages
