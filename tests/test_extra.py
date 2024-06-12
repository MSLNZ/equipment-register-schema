import pytest


def test_invalid_name(xml):
    xml.extra('<not_extra/>')
    xml.raises(r'Expected is .*extra')


def test_more_than_one_occurance(xml):
    xml.extra('<extra/><extra/>')
    xml.raises('This element is not expected')


@pytest.mark.parametrize(
    'attributes',
    [{},
     {'message': 'any number of attributes are allowed'},
     {'a': 0, 'b': 1, 'c': 2, 'd': 3},
     ])
def test_attributes(xml, attributes):
    xml.extra(xml.element('extra', **attributes))
    assert xml.is_valid()


def test_empty_ok(xml):
    xml.extra('<extra/>')
    assert xml.is_valid()


def test_contents_1(xml):
    sub_element = xml.element('extra', text='hi', x=23.1)
    xml.extra(f'<extra>{sub_element}</extra>')
    assert xml.is_valid()


def test_contents_4(xml):
    one = xml.element('one')
    two = xml.element('two', text='something', check=True)
    three = xml.element('three', text='does\nnot\tmatter  \n      ', x=1, y=2, z=3)
    nested = xml.element('nested', text='<four f="4">FOUR</four>')
    xml.extra(f'<extra n="4">'
               f'\n      {one}'
               f'\n      {two}'
               f'\n      {three}'
               f'\n      {nested}'
               f'\n    </extra>')
    assert xml.is_valid()
