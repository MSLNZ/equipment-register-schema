import pytest


def test_no_keywords_attribute(xml):
    xml.equipment('equipment')
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
     'GaugeBlock',
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
    ['thermometer',  # case sensitive
     'DigitalMultiMeter',
     'P R T',
     ])
def test_invalid_keywords_value(xml, value):
    xml.equipment('equipment', keywords=value)
    xml.raises("not an element of the set")


@pytest.mark.parametrize('attrib_name', ['bad', 'invalid'])
def test_invalid_attribute_name(xml, attrib_name):
    xml.equipment('equipment', **{attrib_name: 'DigitalMultiMeter'})
    xml.raises(f'The attribute {attrib_name!r} is not allowed')


@pytest.mark.parametrize('name', ['bad', 'name'])
def test_invalid_element_name(xml, name):
    xml.equipment(name)
    xml.raises(f"{name}': This element is not expected")
