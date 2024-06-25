import pytest


def test_component_invalid_name(xml):
    xml.calibrations(xml.measurand('<report/>'))
    xml.raises(r'Expected is .*component')


@pytest.mark.parametrize('value', ['', '   ', 'Ch1', '*^!@#)', 'any\thi\ng'])
def test_component_valid_attribute_value(xml, value):
    xml.calibrations(xml.measurand(xml.component(name=value)))
    assert xml.is_valid()


@pytest.mark.parametrize('value', ['', '   ', 'Ch1', '*^!@#)', 'any\thi\ng'])
def test_component_name_not_unique_same_measurand(xml, value):
    c1 = xml.component(name=value)
    c2 = xml.component(name='unique')
    c3 = xml.component(name=value)
    xml.calibrations(xml.measurand(f'{c1}\n  {c2}\n  {c3}'))
    xml.raises('Duplicate key-sequence .*uniqueComponentName')


@pytest.mark.parametrize('value', ['', '   ', 'Ch1', '*^!@#)', 'any\thi\ng'])
def test_component_name_not_unique_different_measurand(xml, value):
    m1 = xml.measurand(xml.component(name=value), quantity='Humidity', interval=5)
    m2 = xml.measurand(xml.component(name=value), quantity='Temperature', interval=5)
    xml.calibrations(f'{m1}  {m2}')
    assert xml.is_valid()


def test_component_name_unique_same_measurand(xml):
    c1 = xml.component(name='a')
    c2 = xml.component(name='b')
    c3 = xml.component(name='c')
    xml.calibrations(xml.measurand(f'{c1}\n  {c2}\n  {c3}'))
    assert xml.is_valid()
