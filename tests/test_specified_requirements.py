import pytest


def test_invalid_name(xml):
    xml.specified_requirements('<invalid/>')
    xml.raises(r'Expected is .*specifiedRequirements')


def test_repeated(xml):
    xml.specified_requirements('<specifiedRequirements/><specifiedRequirements/>')
    xml.raises(r'Expected is .*financial')


@pytest.mark.parametrize(
    'attributes',
    [{},
     {'message': 'any number of attributes are allowed'},
     {'a': 0, 'b': 1, 'c': 2, 'd': 3},
     ])
def test_attributes(xml, attributes):
    xml.specified_requirements(xml.element('specifiedRequirements', **attributes))
    assert xml.is_valid()


def test_empty_ok(xml):
    xml.specified_requirements('<specifiedRequirements/>')
    assert xml.is_valid()


def test_contents_1(xml):
    sub_element = xml.element('sub', text='hi', x=23.1)
    xml.specified_requirements(f'<specifiedRequirements>{sub_element}</specifiedRequirements>')
    assert xml.is_valid()


def test_contents_4(xml):
    one = xml.element('one')
    two = xml.element('two', text='something', check=True)
    three = xml.element('three', text='does\nnot\tmatter  \n      ', x=1, y=2, z=3)
    nested = xml.element('nested', text='<four f="4">FOUR</four>')
    xml.specified_requirements(f'<specifiedRequirements n="4">\n'
                            f'    {one}\n'
                            f'    {two}\n'
                            f'    {three}\n'
                            f'    {nested}\n'
                            f'</specifiedRequirements>')
    assert xml.is_valid()
