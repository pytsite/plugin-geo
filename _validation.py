"""Geo Validation Rules
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import validation as _ps_validation


class LocationNonEmpty(_ps_validation.rule.DictPartsNonEmpty):
    """Check if the location structure is not empty.
    """

    def __init__(self, value: dict = None, msg_id: str = None, msg_args: dict = None):
        if not msg_id:
            msg_id = 'geo@validation_geolocationnotempty'

        super().__init__(value, msg_id, msg_args, keys=('lng', 'lat'))


class AddressNonEmpty(_ps_validation.rule.DictPartsNonEmpty):
    """Check if an address structure is empty.
    """

    def __init__(self, value: dict = None, msg_id: str = None, msg_args: dict = None):
        """Init.
        """
        if not msg_id:
            msg_id = 'geo@validation_geoaddressnotempty'

        super().__init__(value, msg_id, msg_args, keys=('address', 'lng', 'lat'))
