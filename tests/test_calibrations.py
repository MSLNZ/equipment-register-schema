import pytest


def test_empty(xml):
    xml.calibrations('')
    assert xml.is_valid()


@pytest.mark.parametrize('occurances', [0, 2, 3, 10])
def test_one_occurance(xml, occurances):
    xml.calibrations(occurances)
    xml.raises('documentation')  # <documentation> must be after <calibrations>


def test_no_attributes(xml):
    xml.calibrations('', quantity='Humidity')
    xml.raises("calibrations', attribute 'quantity'")


def test_subelement(xml):
    xml.calibrations('<measurand quantity="Humidity" unit="%rh" interval="5"/>')
    assert xml.is_valid()


def test_subelement_attribute_unique(xml):
    xml.calibrations('<measurand quantity="Humidity" unit="%rh" interval="5"/>'
                     '<measurand quantity="Temperature" unit="T" interval="5"/>')
    assert xml.is_valid()


@pytest.mark.parametrize('quantity', ['Humidity', 'Temperature'])
def test_subelement_attribute_not_unique(xml, quantity):
    xml.calibrations(f'<measurand quantity="{quantity}" unit="%rh" interval="5"/>'
                     f'<measurand quantity="{quantity}" unit="percentRelative" interval="1"/>')
    xml.raises('Duplicate key-sequence .*uniqueMeasurandQuantity')


@pytest.mark.parametrize(
    ('attribs', 'missing'),
    [({}, 'quantity'),
     ({'quantity': 'Humidity'}, 'unit'),
     ({'quantity': 'Humidity', 'unit': '%rh'}, 'interval'),
     ({'interval': '5', 'quantity': 'Humidity'}, 'unit'),
     ({'interval': '0', 'unit': 'T'}, 'quantity'),
     ({'unit': 'T'}, 'quantity'),
     ])
def test_subelement_missing_attributes(xml, attribs, missing):
    xml.calibrations(xml.element('measurand', **attribs))
    xml.raises(f"attribute '{missing}' is required but missing")


def test_subelement_invalid_name(xml):
    xml.calibrations('<anything/>')
    xml.raises(r'Expected is .*measurand')


def test_subelement_invalid_attribute_name(xml):
    xml.calibrations('<measurand quantity="Humidity" unit="%rh" interval="5" foo="bar"/>')
    xml.raises("measurand', attribute 'foo'")


def test_subelement_invalid_quantity_value(xml):
    xml.calibrations('<measurand quantity="invalid" unit="%rh" interval="5"/>')
    xml.raises('not an element of the set')


def test_subelement_invalid_unit_value(xml):
    xml.calibrations('<measurand quantity="Humidity" unit="" interval="5"/>')
    xml.raises('not accepted by the pattern')


def test_subelement_invalid_interval_value(xml):
    xml.calibrations('<measurand quantity="Humidity" unit="%rh" interval="-1"/>')
    xml.raises('less than the minimum value allowed')
