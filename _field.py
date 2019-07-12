"""PytSite Geo Plugin ODM Fields
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from typing import Union
from frozendict import frozendict
from plugins import odm


class Location(odm.field.Dict):
    """Geo Location Field.
    """

    def __init__(self, name: str, **kwargs):
        default = kwargs.get('default', {
            'lng': 0.0,
            'lat': 0.0,
            'accuracy': 0.0,
            'alt': 0.0,
            'alt_accuracy': 0.0,
            'heading': 0.0,
            'speed': 0.0,
        })

        # Helper for building MongoDB's indexes
        default['geo_point'] = {
            'type': 'Point',
            'coordinates': (default['lng'], default['lat'])
        }

        super().__init__(name, default=default, keys=('lng', 'lat'), **kwargs)

    @property
    def is_empty(self) -> bool:
        return self.get_val()['geo_point']['coordinates'] == (0.0, 0.0)

    def _on_set(self, raw_value: Union[dict, frozendict], **kwargs):
        if isinstance(raw_value, frozendict):
            raw_value = dict(raw_value)

        if isinstance(raw_value, (dict, frozendict)):
            # Checking and setting up all necessary keys
            for k in ('lng', 'lat', 'accuracy', 'alt', 'alt_accuracy', 'heading', 'speed'):
                if k in raw_value:
                    try:
                        raw_value[k] = float(raw_value[k])
                    except ValueError:
                        raw_value[k] = 0.0
                else:
                    raw_value[k] = 0.0

            raw_value['geo_point'] = {
                'type': 'Point',
                'coordinates': (raw_value['lng'], raw_value['lat']),
            }

        elif raw_value is not None:
            raise ValueError("Field '{}': dict or None expected.".format(self.name))

        return super()._on_set(raw_value, **kwargs)


class Address(odm.field.Dict):
    """Geo Address Field
    """

    def __init__(self, name: str, **kwargs):
        """Init.
        """
        default = kwargs.get('default', {
            'lng': 0.0,
            'lat': 0.0,
            'address': '',
        })

        # Helper for building MongoDB's indexes
        default['geo_point'] = {
            'type': 'Point',
            'coordinates': (default['lng'], default['lat'])
        }

        super().__init__(name, default=default, keys=('lng', 'lat', 'address'), **kwargs)

    @property
    def is_empty(self) -> bool:
        v = self.get_val()

        return (v['lng'], v['lat']) == (0.0, 0.0) or not v['address']

    def _on_set(self, raw_value: Union[dict, frozendict], **kwargs) -> dict:
        """Hook
        """
        if isinstance(raw_value, frozendict):
            raw_value = dict(raw_value)

        if isinstance(raw_value, dict):
            # Checking lat and lng
            for k in ('lng', 'lat'):
                if k in raw_value:
                    try:
                        raw_value[k] = float(raw_value[k])
                    except ValueError:
                        raw_value[k] = 0.0
                else:
                    raw_value[k] = 0.0

            # Checking address
            if 'address' in raw_value and not isinstance(raw_value['address'], str):
                raise TypeError("raw_value of field '{}.address' must be a str".format(self.name))

            # Helper for building MongoDB's indexes
            raw_value['geo_point'] = {
                'type': 'Point',
                'coordinates': (raw_value['lng'], raw_value['lat']),
            }

        return super()._on_set(raw_value, **kwargs)


class AdministrativeObject(odm.field.Ref):
    pass


class Country(AdministrativeObject):
    """Country Reference Field
    """

    def __init__(self, name: str, **kwargs):
        """Init
        """
        super().__init__(name, model='geo_country', **kwargs)


class Province(AdministrativeObject):
    """Province Reference Field
    """

    def __init__(self, name: str, **kwargs):
        """Init
        """
        super().__init__(name, model='geo_province', **kwargs)


class City(AdministrativeObject):
    """City Reference Field
    """

    def __init__(self, name: str, **kwargs):
        """Init
        """
        super().__init__(name, model='geo_city', **kwargs)


class District(AdministrativeObject):
    """District Reference Field
    """

    def __init__(self, name: str, **kwargs):
        """Init
        """
        super().__init__(name, model='geo_district', **kwargs)


class Street(AdministrativeObject):
    """Street Reference Field
    """

    def __init__(self, name: str, **kwargs):
        """Init
        """
        super().__init__(name, model='geo_street', **kwargs)


class Building(AdministrativeObject):
    """Building Reference Field
    """

    def __init__(self, name: str, **kwargs):
        """Init
        """
        super().__init__(name, model='geo_building', **kwargs)
