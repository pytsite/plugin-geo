"""Geo Widgets.
"""
from typing import Union as _Union
from frozendict import frozendict as _frozendict
from pytsite import html as _html, validation as _validation
from plugins import widget as _widget
from . import _validation_rule

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Location(_widget.Abstract):
    """Geo Address Input Widget.
    """
    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        if 'default' not in kwargs:
            kwargs['default'] = {
                'lng': 0.0,
                'lat': 0.0,
                'accuracy': 0.0,
                'alt': 0.0,
                'alt_accuracy': 0.0,
                'heading': 0.0,
                'speed': 0.0,
            }

        super().__init__(uid, **kwargs)

        self._autodetect = kwargs.get('autodetect', False)
        self._js_module = 'pytsite-geo-widget-location'
        self._css += ' widget-geo-location'

        # Validation rule for 'required' widget
        if self._required:
            self.clr_rules().add_rules([r for r in self.get_rules() if not isinstance(r, _validation.rule.NonEmpty)])
            self.add_rule(_validation_rule.LocationNonEmpty())

    @property
    def required(self) -> bool:
        return self._required

    @required.setter
    def required(self, value: bool):
        if value:
            self.add_rule(_validation_rule.LocationNonEmpty())
        else:
            # Clear all added NonEmpty and LocationNonEmpty rules
            rules = [r for r in self.get_rules() if not isinstance(r, (
                _validation.rule.NonEmpty,
                _validation_rule.LocationNonEmpty
            ))]
            self.clr_rules().add_rules(rules)

        self._required = value

    @property
    def autodetect(self) -> bool:
        return self._autodetect

    @autodetect.setter
    def autodetect(self, value: bool):
        self._autodetect = value

    def set_val(self, val: _Union[dict, _frozendict], **kwargs):
        """Set value of the widget.
        """
        if val is None:
            self.clr_val()
            return

        if isinstance(val, _frozendict):
            val = dict(val)

        if not isinstance(val, dict):
            raise ValueError("Widget '{}': dict or None expected, while '{}' given.".format(self.name, repr(val)))

        if 'lat' not in val or 'lng' not in val:
            raise ValueError("Widget '{}': 'lat' and 'lng' keys are required.".format(self.uid))

        try:
            val['lng'] = float(val['lng'])
            val['lat'] = float(val['lat'])
        except ValueError:
            raise ValueError("Widget '{}': 'lat' and 'lng' keys should be floats.".format(self.uid))

        return super().set_val(val, **kwargs)

    def _get_element(self, **kwargs) -> _html.Element:
        """Render the widget.
        :param **kwargs:
        """
        inputs = _html.TagLessElement()

        inputs.append(_html.P('Longitude: {}, latitude: {}'.format(self.value['lng'], self.value['lat']), css='text'))

        self._data['autodetect'] = self._autodetect

        for k in ('lng', 'lat', 'coordinates', 'accuracy', 'alt', 'alt_accuracy', 'heading', 'speed'):
            inp_val = self._value[k] if k in self._value else ''
            inputs.append(_html.Input(type='hidden', css=k, name=self._uid + '[' + k + ']', value=inp_val))

        return inputs
