import pytest

from conftest import INVALID_DATES


def test_invalid_name(xml):
    xml.firmware('<invalid/>')
    xml.raises(r'Expected is .*firmware')


def test_repeated(xml):
    xml.firmware('<firmware/><firmware/>')
    xml.raises(r'Expected is .*maintenance')


def test_invalid_attribute(xml):
    xml.firmware('<firmware invalid="1"/>')
    xml.raises("firmware', attribute 'invalid'")


def test_invalid_subelement_name(xml):
    xml.firmware('<firmware><invalid/></firmware>')
    xml.raises(r'Expected is .*version')


def test_version_date_missing(xml):
    xml.firmware('<firmware><version/></firmware>')
    xml.raises("attribute 'date' is required")


def test_invalid_version_attribute_name(xml):
    xml.firmware('<firmware><version invalid="2023-06-14"/></firmware>')
    xml.raises("version', attribute 'invalid'")


@pytest.mark.parametrize('value', INVALID_DATES)
def test_invalid_version_attribute_value(xml, value):
    xml.firmware(f'<firmware><version date="{value}">1.0</version></firmware>')
    xml.raises("atomic type 'xs:date'")


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
     'Version\n1.0',
     'Version\n1\t0',
     'Version\r1.0',
     'Version\r1\t0',
     ])
def test_invalid_version_pattern(xml, text):
    xml.firmware(f'<firmware><version date="2023-06-14">{text}</version></firmware>')
    xml.raises('not accepted by the pattern')


@pytest.mark.parametrize(
    'text',
    ['v1.0',
     '1.0,0.0, 1.98r0',
     ])
def test_valid_version_pattern(xml, text):
    xml.firmware(f'<firmware><version date="2023-06-14">{text}</version></firmware>')
    assert xml.is_valid()


def test_multiple_versions_all_valid(xml):
    xml.firmware('<firmware>'
                 '  <version date="2023-06-19">1.5</version>'
                 '  <version date="2023-06-18">1.4</version>'
                 '  <version date="2023-06-17">1.3</version>'
                 '  <version date="2023-06-16">1.2</version>'
                 '  <version date="2023-06-15">1.1</version>'
                 '</firmware>')
    assert xml.is_valid()


def test_multiple_versions_invalid_text(xml):
    xml.firmware('<firmware>'
                 '  <version date="2023-06-19">1.5</version>'
                 '  <version date="2023-06-18">1.4</version>'
                 '  <version date="2023-06-17"></version>'
                 '  <version date="2023-06-16">1.2</version>'
                 '  <version date="2023-06-15">1.1</version>'
                 '</firmware>')
    xml.raises('not accepted by the pattern')


def test_multiple_versions_invalid_name(xml):
    xml.firmware('<firmware>'
                 '  <version date="2023-06-19">1.5</version>'
                 '  <version date="2023-06-18">1.4</version>'
                 '  <version date="2023-06-17">1.3</version>'
                 '  <invalid date="2023-06-16">1.2</invalid>'
                 '  <version date="2023-06-15">1.1</version>'
                 '</firmware>')
    xml.raises(r'Expected is .*version')


@pytest.mark.parametrize('value', INVALID_DATES)
def test_multiple_versions_invalid_attribute_value(xml, value):
    xml.firmware(f'<firmware>'
                 f'  <version date="2023-06-19">1.5</version>'
                 f'  <version date="2023-06-18">1.4</version>'
                 f'  <version date="{value}">1.3</version>'
                 f'  <version date="2023-06-16">1.2</version>'
                 f'  <version date="2023-06-15">1.1</version>'
                 f'</firmware>')
    xml.raises("atomic type 'xs:date'")


def test_multiple_versions_invalid_attribute_name(xml):
    xml.firmware('<firmware>'
                 '  <version date="2023-06-19">1.5</version>'
                 '  <version date="2023-06-18">1.4</version>'
                 '  <version date="2023-06-17">1.3</version>'
                 '  <version date="2023-06-16">1.2</version>'
                 '  <version invalid="2023-06-15">1.1</version>'
                 '</firmware>')
    xml.raises("version', attribute 'invalid'")
