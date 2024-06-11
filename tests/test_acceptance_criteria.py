import pytest


def test_invalid_name(xml):
    xml.acceptance_criteria('<invalid/>')
    xml.raises(r'Expected is .*acceptanceCriteria')


def test_repeated(xml):
    xml.acceptance_criteria('<acceptanceCriteria/><acceptanceCriteria/>')
    xml.raises(r'Expected is .*documentation')


@pytest.mark.parametrize(
    'attributes',
    [{},
     {'message': 'any number of attributes are allowed'},
     {'a': 0, 'b': 1, 'c': 2, 'd': 3},
     ])
def test_attributes(xml, attributes):
    xml.acceptance_criteria(xml.element('acceptanceCriteria', **attributes))
    assert xml.is_valid()


def test_empty_ok(xml):
    xml.acceptance_criteria('<acceptanceCriteria/>')
    assert xml.is_valid()


def test_contents_1(xml):
    sub_element = xml.element('sub', text='hi', x=23.1)
    xml.acceptance_criteria(f'<acceptanceCriteria>{sub_element}</acceptanceCriteria>')
    assert xml.is_valid()


def test_contents_4(xml):
    one = xml.element('one')
    two = xml.element('two', text='something', check=True)
    three = xml.element('three', text='does\nnot\tmatter  \n      ', x=1, y=2, z=3)
    nested = xml.element('nested', text='<four f="4">FOUR</four>')
    xml.acceptance_criteria(f'<acceptanceCriteria n="4">\n'
                            f'    {one}\n'
                            f'    {two}\n'
                            f'    {three}\n'
                            f'    {nested}\n'
                            f'</acceptanceCriteria>')
    assert xml.is_valid()
