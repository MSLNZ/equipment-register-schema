import pytest

from conftest import XML


@pytest.mark.parametrize(
    'source',
    ['<register></register>',  # no attribute, no namespace
     '<register team="Light"></register>',  # no namespace
     f'<msl:register xmlns:msl="{XML.NAMESPACE}"></msl:register>',  # no attribute
     '<register team="Light" xmlns="invalid.org"></register>',  # invalid namespace
     f'<invalid team="Light" xmlns="{XML.NAMESPACE}"></invalid>',  # invalid name
     f'<msl:registry team="Light" xmlns:msl="{XML.NAMESPACE}"></msl:registry>',  # invalid name
     f'<register x="1" xmlns="{XML.NAMESPACE}"></register>',  # invalid attribute
     f'<register team="Light" x="1" xmlns="{XML.NAMESPACE}"></register>',  # invalid attribute
     f'<msl:register msl:team="Light" xmlns:msl="{XML.NAMESPACE}"></msl:register>',  # invalid attribute namespace
     ])
def test_invalid(xml, source):
    xml.source = source
    assert not xml.is_valid()


@pytest.mark.parametrize(
    'source',
    ['',  # use the default elements in XML.__repr__
     f'<register team="Light" xmlns="{XML.NAMESPACE}"/>',
     f'<register team="Light" xmlns="{XML.NAMESPACE}"></register>',
     f'<m:register team="Light" xmlns:m="{XML.NAMESPACE}"></m:register>',
     f'<msl:register team="Light" xmlns:msl="{XML.NAMESPACE}"></msl:register>',
     ])
def test_valid(xml, source):
    xml.source = source
    assert xml.is_valid()
