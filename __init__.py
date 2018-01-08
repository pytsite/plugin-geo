"""PytSite Geo Package
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import plugman as _plugman

if _plugman.is_installed(__name__):
    # Public API
    from . import _types as types, _widget as widget, _field as field, _validation_rule as validation_rule


def _register_assetman_resources():
    from plugins import assetman

    if not assetman.is_package_registered(__name__):
        assetman.register_package(__name__)
        assetman.t_js(__name__)
        assetman.js_module('pytsite-geo-widget-location', __name__ + '@js/pytsite-geo-widget-location')

    return assetman


def plugin_install():
    _register_assetman_resources().build(__name__)


def plugin_load():
    from pytsite import lang

    lang.register_package(__name__)
    _register_assetman_resources()
