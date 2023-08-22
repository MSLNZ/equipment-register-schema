import pytest


@pytest.mark.parametrize(
    'namespace',
    ['invalid.org',
     'equipment-register',
     'www.measurement.govt.nz/equipment-register',
     'https://www.measurement.govt.nz/'
     'http://www.measurement.govt.nz/equipment-register',  # http not https
     ])
def test_invalid_namespace(xml, namespace):
    xml.root(namespace=namespace, team='Light')
    xml.raises('No matching global declaration')


@pytest.mark.parametrize(
    ('attributes', 'name'),
    [({'namespaces': 'Light'}, 'namespaces'),
     ({'team': 'Light', 'action': 'acquired'}, 'action'),
     ])
def test_invalid_attribute_name(xml, attributes, name):
    xml.root(**attributes)
    xml.raises(f'The attribute {name!r} is not allowed')


@pytest.mark.parametrize(
    'value',
    ['', 'Any', 'Chemistry', ' Light', 'Light ', 'light'])
def test_invalid_attribute_value(xml, value):
    xml.root(team=value)
    xml.raises(f"The value '{value}' is not an element of the set")


@pytest.mark.parametrize(
    'value',
    ['Electrical', 'Humidity', 'Length', 'Light',
     'Mass', 'Pressure', 'Temperature', 'Time'])
def test_valid_attribute_value(xml, value):
    xml.root(team=value)
    assert xml.is_valid()
