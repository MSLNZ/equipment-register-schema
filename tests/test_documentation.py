import pytest


def test_empty(xml):
    xml.quality_manual('<documentation/>')
    assert xml.is_valid()


def test_multiple(xml):
    xml.quality_manual('<documentation/><documentation/>')
    xml.raises(r"documentation': This element is not expected")


def test_no_attributes_allowed(xml):
    xml.quality_manual(xml.element('documentation', x=1))
    xml.raises(r"attribute 'x' is not allowed")


@pytest.mark.parametrize(
    'text',
    [''
     ' ',
     '      ',
     '\r\n\t',
     'a',
     '\n\n\nC a n C o n t a i n   S p   a    c     e       s         !@#$%^*():{}"+_\n\n\n'
])
def test_any_string_content(xml, text):
    xml.quality_manual(xml.element('documentation', text=text))
    assert xml.is_valid()