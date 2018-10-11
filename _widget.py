"""PytSite Geo UI Plugin Widgets
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from typing import Union as _Union
from frozendict import frozendict as _frozendict
from pytsite import html as _html, validation as _validation
from plugins import geo as _geo, widget as _widget, odm as _odm, taxonomy as _taxonomy


class Location(_widget.Abstract):
    """Geo Location Input Widget
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
        self._css += ' widget-geo-location'

        # Validation rule for 'required' widget
        if self._required:
            self.clr_rules().add_rules([r for r in self.get_rules() if not isinstance(r, _validation.rule.NonEmpty)])
            self.add_rule(_geo.validation.LocationNonEmpty())

    @property
    def required(self) -> bool:
        return self._required

    @required.setter
    def required(self, value: bool):
        if value:
            self.add_rule(_geo.validation.LocationNonEmpty())
        else:
            # Clear all added NonEmpty and LocationNonEmpty rules
            rules = [r for r in self.get_rules() if not isinstance(r, (
                _validation.rule.NonEmpty,
                _geo.validation.LocationNonEmpty
            ))]
            self.clr_rules().add_rules(rules)

        self._required = value

    @property
    def autodetect(self) -> bool:
        return self._autodetect

    @autodetect.setter
    def autodetect(self, value: bool):
        self._autodetect = value

    def set_val(self, val: _Union[dict, _frozendict]):
        """Set value of the widget.
        """
        if val is None:
            self.clr_val()
            return

        if isinstance(val, _frozendict):
            val = dict(val)

        if not isinstance(val, dict):
            raise ValueError("Widget '{}': dict or None expected, while '{}' given".format(self.name, repr(val)))

        if 'lat' not in val or 'lng' not in val:
            raise ValueError("Widget '{}': 'lat' and 'lng' keys are required".format(self.uid))

        try:
            val['lng'] = float(val['lng'])
            val['lat'] = float(val['lat'])
        except ValueError:
            raise ValueError("Widget '{}': 'lat' and 'lng' keys should be floats".format(self.uid))

        return super().set_val(val)

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


class AdministrativeSelect(_taxonomy.widget.TermSelectSearch):
    def __init__(self, uid: str, **kwargs):
        """Init
        """
        super().__init__(uid, sort_field='title', **kwargs)

        if self._tags and not self._linked_select:
            raise RuntimeError('You cannot use tags without linked select')

        self._full_title = kwargs.get('full_title', not self._linked_select)
        if self._full_title:
            self._entity_title_args['full_title'] = True

    def set_val(self, value):
        # Value may be not a reference but simple string
        if value and self._tags:
            try:
                # Check if the reference was given
                _odm.resolve_ref(value)
            except _odm.error.InvalidReference:
                from . import _api

                # Search for existing term
                term = _api.find(self._model, value).first()

                # Term not found, create it
                if not term:
                    term = _api.dispense(self._model, value)
                    if self._model == 'geo_province':
                        term.f_set('country', self._linked_select.value)
                    elif self._model == 'geo_city':
                        term.f_set('province', self._linked_select.value)
                    elif self._model == 'geo_district':
                        term.f_set('city', self._linked_select.value)
                    elif self._model == 'geo_street':
                        term.f_set('district', self._linked_select.value)
                    elif self._model == 'geo_building':
                        term.f_set('street', self._linked_select.value)

                value = term.save().ref

        return super().set_val(value)


class CountrySelect(AdministrativeSelect):
    def __init__(self, uid: str, **kwargs):
        """Init
        """
        super().__init__(uid, model='geo_country', **kwargs)


class ProvinceSelect(AdministrativeSelect):
    def __init__(self, uid: str, **kwargs):
        """Init
        """
        country_select = kwargs.get('country_select')
        if isinstance(country_select, CountrySelect):
            kwargs['linked_select'] = country_select

        super().__init__(uid, model='geo_province', **kwargs)


class CitySelect(AdministrativeSelect):
    def __init__(self, uid: str, **kwargs):
        """Init
        """
        province_select = kwargs.get('province_select')
        if isinstance(province_select, ProvinceSelect):
            kwargs['linked_select'] = province_select

        super().__init__(uid, model='geo_city', **kwargs)


class DistrictSelect(AdministrativeSelect):
    def __init__(self, uid: str, **kwargs):
        """Init
        """
        city_select = kwargs.get('city_select')
        if isinstance(city_select, CitySelect):
            kwargs['linked_select'] = city_select

        super().__init__(uid, model='geo_district', **kwargs)


class StreetSelect(AdministrativeSelect):
    def __init__(self, uid: str, **kwargs):
        """Init
        """
        district_select = kwargs.get('district_select')
        if isinstance(district_select, DistrictSelect):
            kwargs['linked_select'] = district_select

        super().__init__(uid, model='geo_street', **kwargs)


class BuildingSelect(AdministrativeSelect):
    def __init__(self, uid: str, **kwargs):
        """Init
        """
        street_select = kwargs.get('street_select')
        if isinstance(street_select, StreetSelect):
            kwargs['linked_select'] = street_select

        super().__init__(uid, model='geo_building', **kwargs)
