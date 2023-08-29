import pytest


def test_no_attribute(xml):
    xml.equipment('equipment')
    assert xml.is_valid()


@pytest.mark.parametrize(
    'value',
    ['DMM',
     'PRT',
     'Resistor',
     'ResistanceBridge',
     'Gauge',
     'GaugeBLockComparator',
     'Laser',
     'Barometer',
     'Humidity',
     'Temperature',
     'TemperatureHumidity',
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
     'dmm',
     ' DMM',
     'DMM ',
     'Resistance-Bridge',
     'Temperature\n',
     'Temperature Humidity',
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
