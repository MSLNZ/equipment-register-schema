import pytest


def test_no_attribute(xml):
    xml.equipment('equipment')
    assert xml.is_valid()


@pytest.mark.parametrize(
    'value',
    ['',
     ' ',
     'can',
     'be any',
     ' xsd:string',
     ])
def test_valid_attribute_value(xml, value):
    xml.equipment('equipment', category=value)
    assert xml.is_valid()


@pytest.mark.parametrize('category', ['bad', 'invalid'])
def test_invalid_attribute_name(xml, category):
    xml.equipment('equipment', **{category: 'DMM'})
    xml.raises(f'The attribute {category!r} is not allowed')


@pytest.mark.parametrize('name', ['bad', 'name'])
def test_invalid_element_name(xml, name):
    xml.equipment(name)
    xml.raises(f"{name}': This element is not expected")
