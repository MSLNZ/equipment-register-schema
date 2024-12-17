import pytest


def test_invalid_name(xml):
    xml.reference_materials('<invalid/>')
    xml.raises(r'Expected is .*referenceMaterials')


def test_repeated(xml):
    xml.reference_materials('<referenceMaterials/><referenceMaterials/>')
    xml.raises(r'Expected is .*documentation')


@pytest.mark.parametrize(
    'attributes',
    [{},
     {'message': 'any number of attributes are allowed'},
     {'a': 0, 'b': 1, 'c': 2, 'd': 3},
     ])
def test_attributes(xml, attributes):
    xml.reference_materials(xml.element('referenceMaterials', **attributes))
    assert xml.is_valid()


def test_empty_ok(xml):
    xml.reference_materials('<referenceMaterials/>')
    assert xml.is_valid()


def test_contents_1(xml):
    sub_element = xml.element('sub', text='hi', x=23.1)
    xml.reference_materials(f'<referenceMaterials>{sub_element}</referenceMaterials>')
    assert xml.is_valid()


def test_contents_4(xml):
    one = xml.element('one')
    two = xml.element('two', text='something', check=True)
    three = xml.element('three', text='does\nnot\tmatter  \n      ', x=1, y=2, z=3)
    nested = xml.element('nested', text='<four f="4">FOUR</four>')
    xml.reference_materials(f'<referenceMaterials n="4">\n'
                            f'    {one}\n'
                            f'    {two}\n'
                            f'    {three}\n'
                            f'    {nested}\n'
                            f'</referenceMaterials>')
    assert xml.is_valid()
