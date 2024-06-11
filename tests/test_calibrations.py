import pytest


def test_empty(xml):
    xml.calibrations('')
    assert xml.is_valid()


@pytest.mark.parametrize('occurances', [0, 2, 3, 10])
def test_one_occurance(xml, occurances):
    xml.calibrations(occurances)
    xml.raises('maintenance')  # <maintenance> must be after <calibrations>


def test_no_attributes(xml):
    xml.calibrations('', quantity='Humidity')
    xml.raises("calibrations', attribute 'quantity'")


def test_measurand_default(xml):
    xml.calibrations(xml.measurand())
    assert xml.is_valid()


def test_measurand_quantity_attribute_unique(xml):
    m1 = xml.measurand(quantity='Humidity', unit='%rh', interval='5')
    m2 = xml.measurand(quantity='Temperature', unit='\u00B0C', interval='5')
    xml.calibrations(f'{m1}  {m2}')
    assert xml.is_valid()


@pytest.mark.parametrize('quantity', ['Humidity', 'Temperature'])
def test_measurand_quantity_attribute_not_unique(xml, quantity):
    m1 = xml.measurand(quantity=quantity, unit='%rh', interval='5')
    m2 = xml.measurand(quantity=quantity, unit='percentRelative', interval='1')
    xml.calibrations(f'{m1}  {m2}')
    xml.raises('Duplicate key-sequence .*uniqueMeasurandQuantity')


@pytest.mark.parametrize(
    ('attribs', 'missing'),
    [({'foo': 'bar'}, ''),
     ({'quantity': 'Humidity'}, 'unit'),
     ({'quantity': 'Humidity', 'unit': '%rh'}, 'interval'),
     ({'interval': '5', 'quantity': 'Humidity'}, 'unit'),
     ({'interval': '0', 'unit': 'T'}, 'quantity'),
     ({'unit': 'T'}, 'quantity'),
     ])
def test_measurand_missing_attributes(xml, attribs, missing):
    xml.calibrations(xml.measurand(**attribs))
    if missing:
        xml.raises(f"measurand': The attribute '{missing}' is required")
    else:
        xml.raises(f"measurand', attribute 'foo'")


def test_measurand_invalid_name(xml):
    xml.calibrations('<anything/>')
    xml.raises(r'Expected is .*measurand')


def test_measurand_invalid_attribute_name(xml):
    xml.calibrations(xml.measurand(
        quantity='Humidity', unit='%rh', interval='5', foo='bar'))
    xml.raises("measurand', attribute 'foo'")


def test_measurand_invalid_quantity_value(xml):
    xml.calibrations(xml.measurand(
        quantity='invalid', unit='%rh', interval='5'))
    xml.raises('not an element of the set')


@pytest.mark.parametrize(
    'unit',
    ['',
     ' ',
     '     ',
     '\t',
     '\n',
     '\r',
     '\n\r',
     '\n\n\n\n',
     '\t\t\t\t\t',
     ' \t\n',
     ])
def test_measurand_invalid_unit_value(xml, unit):
    xml.calibrations(xml.measurand(
        quantity='Humidity', unit=unit, interval='5'))
    xml.raises('not accepted by the pattern')


@pytest.mark.parametrize('unit', ['any', 'a\ny', 'can contain spaces'])
def test_measurand_valid_unit_value(xml, unit):
    xml.calibrations(xml.measurand(
        quantity='Humidity', unit=unit, interval='5'))
    assert xml.is_valid()


@pytest.mark.parametrize('interval', [-1, -0.0001, -9999])
def test_measurand_invalid_interval_value(xml, interval):
    xml.calibrations(xml.measurand(
        quantity='Humidity', unit='%rh', interval=interval))
    xml.raises('less than the minimum value allowed')


@pytest.mark.parametrize('interval', ['1e3', '-1e3', '3.4e0'])
def test_measurand_invalid_interval_atomic(xml, interval):
    xml.calibrations(xml.measurand(
        quantity='Humidity', unit='%rh', interval=interval))
    xml.raises('not a valid value of the atomic type')


@pytest.mark.parametrize('interval', [0, 0.001, 1, 2.3, 56.4119])
def test_measurand_valid_interval_value(xml, interval):
    xml.calibrations(xml.measurand(
        quantity='Humidity', unit='%rh', interval=interval))
    assert xml.is_valid()
