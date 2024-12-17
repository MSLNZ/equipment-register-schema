import pytest

from .conftest import INVALID_DATES


def test_empty(xml):
    xml.quality_manual('<financial/>')
    assert xml.is_valid()


def test_multiple(xml):
    xml.quality_manual('<financial/><financial/>')
    xml.raises(r"financial': This element is not expected")


@pytest.mark.parametrize(
    'asset', [' ', '01234', 'ABC123', ':any-\n@thing '])
def test_asset_number_only(xml, asset):
    xml.quality_manual(xml.financial(asset_number=asset))
    assert xml.is_valid()


def test_warranty_date_only(xml):
    xml.quality_manual(xml.financial(warranty_date='2024-07-23'))
    assert xml.is_valid()


def test_year_purchased_only(xml):
    xml.quality_manual(xml.financial(year_purchased='2024'))
    assert xml.is_valid()


@pytest.mark.parametrize('date', INVALID_DATES)
def test_warranty_date_invalid(xml, date):
    xml.quality_manual(xml.financial(warranty_date=date))
    xml.raises(r"atomic type 'xs:date'")


@pytest.mark.parametrize('year', ['202', '1', '', 'two'])
def test_year_purchased_invalid(xml, year):
    xml.quality_manual(xml.financial(year_purchased=year))
    xml.raises(r"atomic type 'xs:gYear'")


@pytest.mark.parametrize(
    'kwargs',
    [{'yearPurchased': 2025, 'warrantyExpirationDate': '2024-06-29'},
     {'warrantyExpirationDate': '2024-06-29', 'yearPurchased': 2025},
     {'warrantyExpirationDate': '2024-06-29', 'assetNumber': '1', 'yearPurchased': 2025},
     {'yearPurchased': 2025, 'assetNumber': '1'},
     {'assetNumber': '1', 'yearPurchased': 2025},
     ])
def test_any_order(xml, kwargs):
    xml.quality_manual(xml.financial(**kwargs))
    assert xml.is_valid()


@pytest.mark.parametrize(
    'kwargs',
    [{'yearPurchased': 2025, 'unexpected': 'anything'},
     {'unexpected': '2024-06-29', 'yearPurchased': 2025},
     {'warrantyExpirationDate': '2024-06-29', 'assetNumber': '1', 'unexpected': 2025},
     ])
def test_unexpected_element(xml, kwargs):
    xml.quality_manual(xml.financial(**kwargs))
    xml.raises(r"unexpected': This element is not expected")


@pytest.mark.parametrize(
    'kwargs',
    [{'yearPurchased': 2025, 'assetNumber': '1'},
     {'assetNumber': '1'},
     ])
def test_asset_number_repeated(xml, kwargs):
    xml.quality_manual(xml.financial(asset_number='123', **kwargs))
    xml.raises(r"assetNumber': This element is not expected")


@pytest.mark.parametrize(
    'kwargs',
    [{'yearPurchased': 2025, 'warrantyExpirationDate': '2025-01-01'},
     {'warrantyExpirationDate': '2025-01-01'},
     ])
def test_warranty_repeated(xml, kwargs):
    xml.quality_manual(xml.financial(warranty_date='2030-05-19', **kwargs))
    xml.raises(r"warrantyExpirationDate': This element is not expected")


@pytest.mark.parametrize(
    'kwargs',
    [{'warrantyExpirationDate': '2025-01-01', 'yearPurchased': 2025},
     {'yearPurchased': 2025},
     ])
def test_year_purchased_repeated(xml, kwargs):
    xml.quality_manual(xml.financial(year_purchased='1984', **kwargs))
    xml.raises(r"yearPurchased': This element is not expected")
