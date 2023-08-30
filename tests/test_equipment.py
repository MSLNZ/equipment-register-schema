import pytest


def test_no_attribute(xml):
    xml.equipment('equipment')
    assert xml.is_valid()


@pytest.mark.parametrize(
    'value',
    ['DigitalMultiMeter',
     'Resistor',
     'GaugeBlock',
     'Laser',
     'Barometer',
     'Hygrometer',
     'Thermometer',
     ])
def test_valid_attribute_value(xml, value):
    xml.equipment('equipment', category=value)
    assert xml.is_valid()


@pytest.mark.parametrize(
    'value',
    ['',
     ' ',
     '\n',
     '\t',
     '\r',
     '   \t \r  \n',
     'thermometer',
     ' Thermometer',
     'Thermometer ',
     'Thermometer\n',
     'DMM',
     'Digital Multimeter',
     ])
def test_invalid_attribute_value(xml, value):
    xml.equipment('equipment', category=value)
    xml.raises("not an element of the set")


@pytest.mark.parametrize('category', ['bad', 'invalid'])
def test_invalid_attribute_name(xml, category):
    xml.equipment('equipment', **{category: 'DMM'})
    xml.raises(f'The attribute {category!r} is not allowed')


@pytest.mark.parametrize('name', ['bad', 'name'])
def test_invalid_element_name(xml, name):
    xml.equipment(name)
    xml.raises(f"{name}': This element is not expected")
