"""PytSite Geo Plugin API functions
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from plugins import taxonomy, odm as _odm


def find(model: str, title: str = None, alias: str = None, language: str = None) -> _odm.Finder:
    """Find a geo term
    """
    f = taxonomy.find('geo_{}'.format(model), language)

    if title:
        f.regex('title', title, True)

    if alias:
        f.eq('alias', alias)

    return f


def find_country(title: str = None, alias: str = None, language: str = None) -> _odm.Finder:
    """Find country
    """
    return find('country', title, alias, language)


def find_province(title: str = None, alias: str = None, language: str = None) -> _odm.Finder:
    """Find province
    """
    return find('province', title, alias, language)


def find_city(title: str = None, alias: str = None, language: str = None) -> _odm.Finder:
    """Find city
    """
    return find('city', title, alias, language)


def find_district(title: str = None, alias: str = None, language: str = None) -> _odm.Finder:
    """Find district
    """
    return find('district', title, alias, language)


def find_street(title: str = None, alias: str = None, language: str = None) -> _odm.Finder:
    """Find street
    """
    return find('street', title, alias, language)


def find_building(title: str = None, alias: str = None, language: str = None) -> _odm.Finder:
    """Find building
    """
    return find('building', title, alias, language)
