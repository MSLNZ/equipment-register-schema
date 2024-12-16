import pytest

from tests.conftest import INVALID_DATES


def test_unexpected_element(xml):
    xml.calibrations(xml.measurand(xml.component('<unexpected>comment</unexpected>')))
    xml.raises(r"unexpected': This element is not expected")


def test_date_missing(xml):
    xml.calibrations(xml.measurand(xml.component('<adjustment>comment</adjustment>')))
    xml.raises(r"attribute 'date' is required but missing")


@pytest.mark.parametrize('date', INVALID_DATES)
def test_date_invalid(xml, date):
    adj = f'<adjustment date="{date}">comment</adjustment>'
    xml.calibrations(xml.measurand(xml.component(adj)))
    xml.raises(r"not a valid value of the atomic type")


@pytest.mark.parametrize('date', ["1999-12-19", "2100-01-01"])
def test_date_valid(xml, date):
    adj = f'<adjustment date="{date}">comment</adjustment>'
    xml.calibrations(xml.measurand(xml.component(adj)))
    assert xml.is_valid()


@pytest.mark.parametrize(
    'text',
    ['',
     ' ',
     '       ',
     '\t',
     '\t         ',
     '\r',
     '\n',
     ' \t\n \r ',
     'Cleaned\nthe filter',
     'Cleaned\nthe\tfilter',
     'Cleaned\rthe filter',
     'Cleaned\rthe\tfilter',
])
def test_text_invalid(xml, text):
    adj = f'<adjustment date="2024-10-17">{text}</adjustment>'
    xml.calibrations(xml.measurand(xml.component(adj)))
    xml.raises('not accepted by the pattern')


@pytest.mark.parametrize(
    'text',
    ['a',
     ' a',
     'a ',
     '  a     ',
     'Cleaned the filter',
     ' Cleaned the    filter',
     'Cleaned\tthe\tfilter',
     'The filter was dirty so it was cleaned an then another set of measurements were acquired',
])
def test_text_valid(xml, text):
    adj = f'<adjustment date="2024-10-17">{text}</adjustment>'
    xml.calibrations(xml.measurand(xml.component(adj)))
    assert xml.is_valid()


def test_multiple(xml):
    adj = '<adjustment date="2024-10-17">Cleaned the filter</adjustment>'
    xml.calibrations(xml.measurand(xml.component(f'{adj}{adj}{adj}{adj}')))
    assert xml.is_valid()
