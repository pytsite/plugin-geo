"""PytSite Geo Plugin Types
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from typing import List as _List


class Abstract:
    def as_jsonable(self):
        raise NotImplementedError()

    def __str__(self) -> str:
        return str(self.as_jsonable())


class Location(Abstract):
    """Latitude/Longitude Point
    """

    def __init__(self, lat: float, lng: float):
        self._lat = lat
        self._lng = lng

    @property
    def lat(self) -> float:
        return self._lat

    @property
    def lng(self) -> float:
        return self._lng

    def __str__(self):
        return '{},{}'.format(self._lat, self._lng)

    def as_jsonable(self) -> dict:
        return {
            'lat': self._lat,
            'lng': self._lng,
        }


class LocationFromDict(Location):
    def __init__(self, data: dict):
        super().__init__(float(data.get('lat', 50.4501)), float(data.get('lng', 30.5234)))


class ViewPort(Abstract):
    def __init__(self, data: dict):
        self._northeast = LocationFromDict(data.get('northeast', {}))
        self._southwest = LocationFromDict(data.get('southwest', {}))

    @property
    def northeast(self) -> Location:
        return self._northeast

    @property
    def southwest(self) -> Location:
        return self._southwest

    def as_jsonable(self) -> dict:
        return {
            'northeast': self._northeast.as_jsonable(),
            'southwest': self._southwest.as_jsonable(),
        }


class Geometry(Abstract):
    def __init__(self, data: dict):
        self._location = LocationFromDict(data.get('location', {}))
        self._location_type = data.get('location_type', '')
        self._viewport = ViewPort(data.get('viewport', {}))

    @property
    def location(self) -> Location:
        return self._location

    @property
    def location_type(self) -> str:
        return self._location_type

    @property
    def viewport(self) -> ViewPort:
        return self._viewport

    def as_jsonable(self) -> dict:
        return {
            'location': self._location.as_jsonable(),
            'location_type': self._location_type,
            'viewport': self._viewport.as_jsonable(),
        }


class AddressComponent(Abstract):
    def __init__(self, data: dict):
        self._long_name = data.get('long_name')
        self._short_name = data.get('short_name')
        self._types = data.get('types', [])

    @property
    def long_name(self) -> str:
        return self._long_name

    @property
    def short_name(self) -> str:
        return self._short_name

    @property
    def types(self) -> _List[str]:
        return self._types

    def as_jsonable(self) -> dict:
        return {
            'long_name': self._long_name,
            'short_name': self._short_name,
            'types': self._types,
        }


class GeocodingResult(Abstract):
    def __init__(self, data: dict):
        self._place_id = data.get('place_id', '')
        self._formatted_address = data.get('formatted_address', '')
        self._types = data.get('types', [])
        self._address_components = [AddressComponent(d) for d in data.get('address_components', [])]
        self._geometry = Geometry(data.get('geometry', {}))

    @property
    def place_id(self) -> str:
        return self._place_id

    @property
    def formatted_address(self) -> str:
        return self._formatted_address

    @property
    def types(self) -> _List[str]:
        return self._types

    @property
    def address_components(self) -> _List[AddressComponent]:
        return self._address_components

    @property
    def geometry(self) -> Geometry:
        return self._geometry

    def as_jsonable(self) -> dict:
        return {
            'place_id': self._place_id,
            'formatted_address': self._formatted_address,
            'types': self._types,
            'address_components': [i.as_jsonable() for i in self._address_components],
            'geometry': self._geometry.as_jsonable(),
        }


class GeocodingResults(Abstract):
    def __init__(self, data: _List[dict]):
        self._results = [GeocodingResult(d) for d in data]

    def results(self) -> _List[GeocodingResult]:
        return self._results

    def __iter__(self):
        return iter(self._results)

    def as_jsonable(self) -> list:
        return [i.as_jsonable() for i in self._results]


class TimeZone(Abstract):
    def __init__(self, data: dict):
        self._dst_offset = data.get('dstOffset')
        self._raw_offset = data.get('rawOffset')
        self._time_zone_id = data.get('timeZoneId')
        self._time_zone_name = data.get('timeZoneName')

    @property
    def dst_offset(self) -> int:
        return self._dst_offset

    @property
    def raw_offset(self) -> int:
        return self._raw_offset

    @property
    def time_zone_id(self) -> str:
        return self._time_zone_id

    @property
    def time_zone_name(self) -> str:
        return self._time_zone_name

    def as_jsonable(self) -> dict:
        return {
            'dst_offset': self._dst_offset,
            'raw_offset': self._raw_offset,
            'time_zone_id': self._time_zone_id,
            'time_zone_name': self._time_zone_name,
        }
