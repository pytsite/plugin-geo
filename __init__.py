"""PytSite Geo Package
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Public API
from . import _types as types, _field as field, _validation as validation, _model as model, _widget as widget
from ._api import dispense, find, find_country, find_province, find_city, find_district, find_street, find_building


def plugin_load():
    from plugins import taxonomy, admin
    from . import _model

    admin.sidebar.add_section('geo', 'geo@geo')

    taxonomy.register_model('geo_country', _model.Country, __name__ + '@countries',
                            menu_icon='fa fas fa-globe', menu_sid='geo')
    taxonomy.register_model('geo_province', _model.Province, __name__ + '@provinces', menu_sid='geo',
                            menu_icon='fa fas fa-map')
    taxonomy.register_model('geo_city', _model.City, __name__ + '@cities', menu_sid='geo',
                            menu_icon='fa fas fa-university')
    taxonomy.register_model('geo_district', _model.District, __name__ + '@districts', menu_sid='geo',
                            menu_icon='fa fas fa-map-marker')
    taxonomy.register_model('geo_street', _model.Street, __name__ + '@streets',
                            menu_icon='fa fas fa-road', menu_sid='geo')
    taxonomy.register_model('geo_building', _model.Building, __name__ + '@buildings',
                            menu_icon='fa fas fa-building', menu_sid='geo')
