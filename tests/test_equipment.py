import pytest


@pytest.mark.parametrize(
    'value',
    ['',
     '        ',
     '   \t \r  \n',
     'Motor',
     'An alias to associate with the equipment!',
     ])
def test_alias(xml, value):
    xml.equipment('equipment', alias=value)
    assert xml.is_valid()


@pytest.mark.parametrize(
    'value',
    ['',
     ' ',
     '\n',
     '\t',
     '\r',
     '   \t \r  \n',
     'DMM',
     '  PRT   ',
     'Gauge Block',
     'Laser\n',
     'Barometer\t',
     'Hygrometer ',
     '      Thermometer',
     'Source  Voltage\t AC\nDC ',
     ])
def test_valid_keywords_value(xml, value):
    xml.equipment('equipment', keywords=value)
    assert xml.is_valid()


@pytest.mark.parametrize(
    'value',
    ['thermometer',  # case-sensitive
     'DigitalMultiMeter',
     'P R T',
     ])
def test_invalid_keywords_value(xml, value):
    xml.equipment('equipment', keywords=value)
    xml.raises("not an element of the set")


@pytest.mark.parametrize('attrib_name', ['bad', 'invalid', 'aliases', 'keyword'])
def test_invalid_attribute_name(xml, attrib_name):
    xml.equipment('equipment', **{attrib_name: 'DigitalMultiMeter'})
    xml.raises(f'The attribute {attrib_name!r} is not allowed')


@pytest.mark.parametrize('name', ['bad', 'name'])
def test_invalid_element_name(xml, name):
    xml.equipment(name)
    xml.raises(f"{name}': This element is not expected")


def test_entered_by_missing(xml):
    xml.equipment('equipment', auto_add_entered_by=False)
    xml.raises("attribute 'enteredBy' is required")


@pytest.mark.parametrize('name', ['', '    '])
def test_entered_by_empty_string(xml, name):
    xml.equipment('equipment', enteredBy=name)
    xml.raises('not accepted by the pattern')


@pytest.mark.parametrize('name', ['me', '', '    '])
def test_checked_by(xml, name):
    xml.equipment('equipment', checkedBy=name)
    assert xml.is_valid()


def test_checked_date_valid(xml):
    xml.equipment('equipment', checkedDate="2025-08-06")
    assert xml.is_valid()


def test_checked_date_invalid(xml):
    xml.equipment('equipment', checkedDate="06-2025-08")
    xml.raises('not a valid value')