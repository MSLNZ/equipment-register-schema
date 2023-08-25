import pytest


def test_invalid_name(xml):
    xml.custom('<not_custom/>')
    xml.raises(r'Expected is \( .*custom \)')


def test_more_than_one_occurance(xml):
    xml.custom('<custom/><custom/>')
    xml.raises('This element is not expected')


@pytest.mark.parametrize(
    'attributes',
    [{},
     {'message': 'any number of attributes are allowed'},
     {'a': 0, 'b': 1, 'c': 2, 'd': 3},
     ])
def test_attributes(xml, attributes):
    xml.custom(xml.element('custom', **attributes))
    assert xml.is_valid()


def test_empty_ok(xml):
    xml.custom('<custom/>')
    assert xml.is_valid()


def test_contents_1(xml):
    sub_element = xml.element('custom', text='hi', x=23.1)
    xml.custom(f'<custom>{sub_element}</custom>')
    assert xml.is_valid()


def test_contents_4(xml):
    one = xml.element('one')
    two = xml.element('two', text='something', check=True)
    three = xml.element('three', text='does\nnot\tmatter  \n      ', x=1, y=2, z=3)
    nested = xml.element('nested', text='<four f="4">FOUR</four>')
    xml.custom(f'<custom n="4">'
               f'\n      {one}'
               f'\n      {two}'
               f'\n      {three}'
               f'\n      {nested}'
               f'\n    </custom>')
    assert xml.is_valid()
