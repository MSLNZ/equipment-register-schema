import pytest


def test_empty(xml):
    xml.quality_manual('<accessories/>')
    assert xml.is_valid()


def test_multiple(xml):
    xml.quality_manual('<accessories/><accessories/>')
    xml.raises(r"accessories': This element is not expected")


@pytest.mark.parametrize(
    'attributes',
    [{},
     {'message': 'any number of attributes are allowed'},
     {'a': 0, 'b': 1, 'c': 2, 'd': 3},
     ])
def test_attributes(xml, attributes):
    xml.quality_manual(xml.element('accessories', **attributes))
    assert xml.is_valid()


def test_contents_1(xml):
    sub_element = xml.element('accessories', text='hi', x=23.1)
    xml.quality_manual(f'<accessories>{sub_element}</accessories>')
    assert xml.is_valid()


def test_contents_4(xml):
    one = xml.element('one')
    two = xml.element('two', text='something', check=True)
    three = xml.element('three', text='does\nnot\tmatter  \n      ', x=1, y=2, z=3)
    nested = xml.element('nested', text='<four f="4">FOUR</four>')
    xml.quality_manual(f'<accessories n="4">'
                       f'\n      {one}'
                       f'\n      {two}'
                       f'\n      {three}'
                       f'\n      {nested}'
                       f'\n    </accessories>')
    assert xml.is_valid()
