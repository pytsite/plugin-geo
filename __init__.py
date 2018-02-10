"""PytSite Geo Package
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Public API
from . import _types as types, _field as field, _validation as validation


def plugin_load():
    from pytsite import lang

    lang.register_package(__name__)
