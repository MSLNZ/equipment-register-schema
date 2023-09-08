import pytest


def test_subelement_invalid_name(xml):
    xml.calibrations(xml.measurand('<report/>'))
    xml.raises(r'Expected is .*component')


@pytest.mark.parametrize('value', ['', '   ', 'Ch1', '*^!@#)', 'any\thi\ng'])
def test_component_valid_attribute_value(xml, value):
    xml.calibrations(xml.measurand(xml.component(name=value)))
    assert xml.is_valid()


@pytest.mark.parametrize('value', ['', '   ', 'Ch1', '*^!@#)', 'any\thi\ng'])
def test_component_name_not_unique(xml, value):
    c1 = xml.component(name=value)
    c2 = xml.component(name='unique')
    c3 = xml.component(name=value)
    xml.calibrations(xml.measurand(f'{c1}\n  {c2}\n  {c3}'))
    xml.raises('Duplicate key-sequence .*uniqueComponentName')


def test_component_name_unique(xml):
    c1 = xml.component(name='a')
    c2 = xml.component(name='b')
    c3 = xml.component(name='c')
    xml.calibrations(xml.measurand(f'{c1}\n  {c2}\n  {c3}'))
    assert xml.is_valid()
