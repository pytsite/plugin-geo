"""Geo Administrative PytSite Plugin ODM Models
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from typing import Union
from decimal import Decimal
from plugins import odm, odm_ui, tag, form, widget
from . import _field, _widget


class AministrativeObject(tag.Tag):
    def _setup_fields(self):
        super()._setup_fields()

        self.remove_field('weight')

        self.define_field(odm.field.Decimal('lng'))
        self.define_field(odm.field.Decimal('lat'))

    @property
    def lng(self) -> Decimal:
        return self.f_get('lng')

    @lng.setter
    def lng(self, value: Union[Decimal, float, int, str]):
        self.f_set('lng', value)

    @property
    def lat(self) -> Decimal:
        return self.f_get('lat')

    @lat.setter
    def lat(self, value: Union[Decimal, float, int, str]):
        self.f_set('lat', value)

    def odm_ui_m_form_setup_widgets(self, frm: form.Form):
        super().odm_ui_m_form_setup_widgets(frm)

        frm.get_widget('title').h_size = 'col-12 col-xs-12 col-lg-6'
        frm.get_widget('alias').h_size = 'col-12 col-xs-12 col-lg-6'

        frm.add_widget(widget.input.Decimal(
            uid='lng',
            weight=350,
            label=self.t('longitude'),
            min=-180.0,
            max=180.0,
            required=self.get_field('lng').is_required,
            h_size='col-12 col-xs-12 col-sm-2 col-lg-1',
            value=self.lng,
        ))

        frm.add_widget(widget.input.Decimal(
            uid='lat',
            weight=355,
            label=self.t('latitude'),
            min=-90.0,
            max=90.0,
            required=self.get_field('lng').is_required,
            h_size='col-12 col-xs-12 col-sm-2 col-lg-1',
            value=self.lat,
        ))

    def odm_ui_widget_select_search_entities(self, f: odm.MultiModelFinder, args: dict):
        super().odm_ui_widget_select_search_entities(f, args)

        # Handle linked selects
        for k, v in args.items():
            if k.startswith('geo_'):
                f_name = k.replace('geo_', '')
                try:
                    if self.has_field(f_name) and v:
                        f.eq(f_name, v)
                except odm.error.InvalidReference as e:
                    pass


class Country(AministrativeObject):
    """Country Term
    """

    def odm_ui_widget_select_search_entities_title(self, args: dict) -> str:
        return self.title


class Province(AministrativeObject):
    """Province Term
    """

    def _setup_fields(self):
        super()._setup_fields()

        self.define_field(_field.Country('country', is_required=True))

    def _on_pre_save(self, **kwargs):
        """Hook
        """
        if not self.alias:
            self.f_set('alias', '{}-{}'.format(self.title, self.country.alias))

        super()._on_pre_save(**kwargs)

    @property
    def country(self) -> Country:
        return self.f_get('country')

    @country.setter
    def country(self, value: Country):
        self.f_set('country', value)

    def odm_ui_browser_setup(self, browser: odm_ui.Browser):
        super().odm_ui_browser_setup(browser)

        browser.default_sort_field = 'title'
        browser.insert_data_field('country', 'geo@country')

    def odm_ui_browser_row(self) -> dict:
        r = super().odm_ui_browser_row()

        r['country'] = self.country.title

        return r

    def odm_ui_m_form_setup_widgets(self, frm: form.Form):
        super().odm_ui_m_form_setup_widgets(frm)

        frm.add_widget(_widget.CountrySelect(
            uid='country',
            weight=50,
            label=self.t('country'),
            h_size='col-12 col-xs-12 col-lg-6',
            required=self.get_field('country').is_required,
            value=self.country,
        ))

    def odm_ui_widget_select_search_entities_title(self, args: dict) -> str:
        if args.get('full_title'):
            return '{}, {}'.format(self.title, self.country.title)
        else:
            return self.title


class City(AministrativeObject):
    """City Term
    """

    def _setup_fields(self):
        super()._setup_fields()

        self.define_field(_field.Province('province', is_required=True))

    def _on_pre_save(self, **kwargs):
        """Hook
        """
        if not self.alias:
            self.f_set('alias', '{}-{}'.format(self.title, self.province.alias))

        super()._on_pre_save(**kwargs)

    @property
    def province(self) -> Province:
        return self.f_get('province')

    @province.setter
    def province(self, value: Province):
        self.f_set('province', value)

    @property
    def country(self) -> Country:
        return self.province.country

    def odm_ui_browser_setup(self, browser: odm_ui.Browser):
        super().odm_ui_browser_setup(browser)

        browser.default_sort_field = 'title'
        browser.insert_data_field('province', 'geo@province')
        browser.insert_data_field('country', 'geo@country')

    def odm_ui_browser_row(self) -> dict:
        r = super().odm_ui_browser_row()

        r['province'] = self.province.title
        r['country'] = self.country.title

        return r

    def odm_ui_m_form_setup_widgets(self, frm: form.Form):
        super().odm_ui_m_form_setup_widgets(frm)

        frm.add_widget(_widget.ProvinceSelect(
            uid='province',
            weight=50,
            label=self.t('province'),
            h_size='col-12 col-xs-12 col-lg-6',
            required=self.get_field('province').is_required,
            value=self.province,
        ))

    def odm_ui_widget_select_search_entities_title(self, args: dict) -> str:
        if args.get('full_title'):
            return '{}, {}, {}'.format(self.title, self.province.title, self.country.title)
        else:
            return self.title


class District(AministrativeObject):
    """District Term
    """

    def _setup_fields(self):
        super()._setup_fields()

        self.define_field(_field.City('city', is_required=True))

    def _on_pre_save(self, **kwargs):
        """Hook
        """
        if not self.alias:
            self.f_set('alias', '{}-{}'.format(self.title, self.city.alias))

        super()._on_pre_save(**kwargs)

    @property
    def city(self) -> City:
        return self.f_get('city')

    @city.setter
    def city(self, value: City):
        self.f_set('city', value)

    @property
    def province(self) -> Province:
        return self.city.province

    @property
    def country(self) -> Country:
        return self.city.country

    def odm_ui_browser_setup(self, browser: odm_ui.Browser):
        super().odm_ui_browser_setup(browser)

        browser.default_sort_field = 'title'
        browser.insert_data_field('city', 'geo@city')
        browser.insert_data_field('province', 'geo@province')
        browser.insert_data_field('country', 'geo@country')

    def odm_ui_browser_row(self) -> dict:
        r = super().odm_ui_browser_row()

        r['city'] = self.city.title
        r['province'] = self.province.title
        r['country'] = self.country.title

        return r

    def odm_ui_m_form_setup_widgets(self, frm: form.Form):
        super().odm_ui_m_form_setup_widgets(frm)

        frm.add_widget(_widget.CitySelect(
            uid='city',
            weight=50,
            label=self.t('city'),
            h_size='col-12 col-xs-12 col-lg-6',
            required=self.get_field('city').is_required,
            value=self.city,
        ))

    def odm_ui_widget_select_search_entities_title(self, args: dict) -> str:
        if args.get('full_title'):
            return '{}, {}, {}, {}'.format(self.title, self.city.title, self.province.title, self.country.title)
        else:
            return self.title


class Street(AministrativeObject):
    """Street Term
    """

    def _setup_fields(self):
        super()._setup_fields()

        self.define_field(_field.District('district', is_required=True))

    def _on_pre_save(self, **kwargs):
        """Hook
        """
        if not self.alias:
            self.f_set('alias', '{}-{}'.format(self.title, self.district.alias))

        super()._on_pre_save(**kwargs)

    @property
    def district(self) -> District:
        return self.f_get('district')

    @district.setter
    def district(self, value: District):
        self.f_set('district', value)

    @property
    def city(self) -> City:
        return self.district.city

    @property
    def province(self) -> Province:
        return self.district.province

    @property
    def country(self) -> Country:
        return self.district.country

    def odm_ui_browser_setup(self, browser: odm_ui.Browser):
        super().odm_ui_browser_setup(browser)

        browser.default_sort_field = 'title'
        browser.insert_data_field('district', 'geo@district')
        browser.insert_data_field('city', 'geo@city')
        browser.insert_data_field('province', 'geo@province')
        browser.insert_data_field('country', 'geo@country')

    def odm_ui_browser_row(self) -> dict:
        r = super().odm_ui_browser_row()

        r['district'] = self.district.title
        r['city'] = self.city.title
        r['province'] = self.province.title
        r['country'] = self.country.title

        return r

    def odm_ui_m_form_setup_widgets(self, frm: form.Form):
        super().odm_ui_m_form_setup_widgets(frm)

        frm.add_widget(_widget.DistrictSelect(
            uid='district',
            weight=50,
            label=self.t('district'),
            h_size='col-12 col-xs-12 col-lg-6',
            required=self.get_field('district').is_required,
            value=self.district,
        ))

    def odm_ui_widget_select_search_entities_title(self, args: dict) -> str:
        if args.get('full_title'):
            return '{}, {}, {}, {}, {}'.format(self.title, self.district.title, self.city.title, self.province.title,
                                               self.country.title)
        else:
            return self.title


class Building(AministrativeObject):
    """Street Term
    """

    def _setup_fields(self):
        super()._setup_fields()

        self.define_field(_field.Street('street', is_required=True))

    def _on_pre_save(self, **kwargs):
        """Hook
        """
        if not self.alias:
            self.f_set('alias', '{}-{}'.format(self.title, self.street.alias))

        super()._on_pre_save(**kwargs)

    @property
    def street(self) -> Street:
        return self.f_get('street')

    @street.setter
    def street(self, value: Street):
        self.f_set('street', value)

    @property
    def district(self) -> District:
        return self.street.district

    @property
    def city(self) -> City:
        return self.district.city

    @property
    def province(self) -> Province:
        return self.city.province

    @property
    def country(self) -> Country:
        return self.province.country

    def odm_ui_browser_setup(self, browser: odm_ui.Browser):
        super().odm_ui_browser_setup(browser)

        browser.default_sort_field = 'title'
        browser.insert_data_field('street', 'geo@street')
        browser.insert_data_field('district', 'geo@district')
        browser.insert_data_field('city', 'geo@city')
        browser.insert_data_field('province', 'geo@province')
        browser.insert_data_field('country', 'geo@country')

    def odm_ui_browser_row(self) -> dict:
        r = super().odm_ui_browser_row()

        r['street'] = self.street.title
        r['district'] = self.district.title
        r['city'] = self.city.title
        r['province'] = self.province.title
        r['country'] = self.country.title

        return r

    def odm_ui_m_form_setup_widgets(self, frm: form.Form):
        super().odm_ui_m_form_setup_widgets(frm)

        frm.add_widget(_widget.StreetSelect(
            uid='street',
            weight=50,
            label=self.t('street'),
            h_size='col-12 col-xs-12 col-lg-6',
            required=self.get_field('street').is_required,
            value=self.street,
        ))

    def odm_ui_widget_select_search_entities_title(self, args: dict) -> str:
        if args.get('full_title'):
            return '{}, {}, {}, {}, {}, {}'.format(self.title, self.street.title, self.district.title, self.city.title,
                                                   self.province.title, self.country.title)
        else:
            return self.title
