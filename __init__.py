"""PytSite Geo Package
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import plugman as _plugman

if _plugman.is_installed(__name__):
    # Public API
    from . import _widget as widget, _field as field, _validation_rule as validation_rule


def plugin_load():
    from pytsite import lang
    from plugins import assetman

    lang.register_package(__name__)

    assetman.register_package(__name__)
    assetman.t_js(__name__)
    assetman.js_module('pytsite-geo-widget-location', __name__ + '@js/pytsite-geo-widget-location')


def plugin_install():
    from plugins import assetman

    plugin_load()
    assetman.build(__name__)
