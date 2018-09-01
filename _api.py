"""PytSite Geo Plugin API functions
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from plugins import taxonomy as _taxonomy, odm as _odm
from . import _model

_GEO_MODELS = ('geo_country', 'geo_province', 'geo_city', 'geo_district', 'geo_street', 'geo_building')


def dispense(model: str, title: str, alias: str = None, language: str = None) -> _model.AministrativeObject:
    """Dispense a geo term
    """
    if model not in _GEO_MODELS:
        raise ValueError("Model '{}' is not in {}".format(model, _GEO_MODELS))

    term = _taxonomy.dispense(model, title, alias, language)  # type: _model.AministrativeObject

    return term


def find(model: str, title: str = None, alias: str = None, language: str = None) -> _odm.Finder:
    """Find a geo term
    """
    f = _taxonomy.find(model.format(model), language)

    if title:
        f.regex('^title$', title, True)

    if alias:
        f.eq('alias', alias)

    return f


def find_country(title: str = None, alias: str = None, language: str = None) -> _odm.Finder:
    """Find country
    """
    return find('geo_country', title, alias, language)


def find_province(title: str = None, alias: str = None, language: str = None) -> _odm.Finder:
    """Find province
    """
    return find('geo_province', title, alias, language)


def find_city(title: str = None, alias: str = None, language: str = None) -> _odm.Finder:
    """Find city
    """
    return find('geo_city', title, alias, language)


def find_district(title: str = None, alias: str = None, language: str = None) -> _odm.Finder:
    """Find district
    """
    return find('geo_district', title, alias, language)


def find_street(title: str = None, alias: str = None, language: str = None) -> _odm.Finder:
    """Find street
    """
    return find('geo_street', title, alias, language)


def find_building(title: str = None, alias: str = None, language: str = None) -> _odm.Finder:
    """Find building
    """
    return find('geo_building', title, alias, language)
