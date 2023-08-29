import pytest


@pytest.mark.parametrize(
    'text',
    ['A',
     'This is a long description that contains only valid characters',
     'A thermometer that can only measure in \u00B0C',
     'any of these characters -,.{}!=-+()*^%$#@!;:',
     ])
def test_valid_pattern(xml, text):
    xml.description(text)
    assert xml.is_valid()


@pytest.mark.parametrize(
    'text',
    ['',
     ' ',
     '           ',
     '\t',
     '\n',
     '\r',
     '  leading spaces',
     'trailing space ',
     'multiple  spaces',
     'new\nline',
     'carriage return\r',
     'contains\tab',
     ])
def test_invalid_pattern(xml, text):
    xml.description(text)
    xml.raises('not accepted by the pattern')


@pytest.mark.parametrize('occurances', [0, 2, 3, 10])
def test_one_occurance(xml, occurances):
    xml.description(occurances)
    xml.raises('active')  # <active> must be after <description>


def test_no_attributes(xml):
    xml.description('A 6.5 digit digital multimeter', foo='bar')
    xml.raises("attribute 'foo' is not allowed")
