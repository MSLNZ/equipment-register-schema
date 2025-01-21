import pytest


def test_invalid_name(xml):
    xml.specifications('<invalid/>')
    xml.raises(r'Expected is .*specifications')


def test_repeated(xml):
    xml.specifications('<specifications/><specifications/>')
    xml.raises(r'Expected is .*location')


def test_element_only(xml):
    xml.specifications('<specifications>text</specifications>')
    xml.raises(r"content type is 'element-only'")


@pytest.mark.parametrize(
    'attributes',
    [{},
     {'message': 'any number of attributes are allowed'},
     {'a': 0, 'b': 1, 'c': 2, 'd': 3},
     ])
def test_attributes(xml, attributes):
    xml.specifications(xml.element('specifications', **attributes))
    assert xml.is_valid()


def test_empty_ok(xml):
    xml.specifications('<specifications/>')
    assert xml.is_valid()


def test_contents_1(xml):
    sub_element = xml.element('sub', text='hi', x=23.1)
    xml.specifications(f'<specifications>{sub_element}</specifications>')
    assert xml.is_valid()


def test_contents_4(xml):
    one = xml.element('one')
    two = xml.element('two', text='something', check=True)
    three = xml.element('three', text='does\nnot\tmatter  \n      ', x=1, y=2, z=3)
    nested = xml.element('nested', text='<four f="4">FOUR</four>')
    xml.specifications(f'<specifications n="4">\n'
                       f'    {one}\n'
                       f'    {two}\n'
                       f'    {three}\n'
                       f'    {nested}\n'
                       f'</specifications>')
    assert xml.is_valid()
