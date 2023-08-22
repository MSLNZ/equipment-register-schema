import pytest


@pytest.mark.parametrize(
    'text',
    ['Company',
     'Company A',
     'Company, ABC.',
     '3m',
     'm3',
     '-,.{}!=-+()*^%$#@!;:',
     'Temperature (\u00B0C)',
     'Temperature (°C)',
     'A     B',
     ])
def test_valid_pattern(xml, text):
    xml.manufacturer(text)
    assert xml.is_valid()


@pytest.mark.parametrize(
    'text',
    ['',
     ' ',
     'a',  # must be at least 2 characters
     'a ',
     ' a',
     '\ta',
     'a\n',
     '     ',
     '\t',
     '\n',
     '\r',
     '\n\r',
     '\n\n\n\n',
     '\t\t\t\t\t',
     ' \t\n',
     ' Company',
     'Company   ',
     '\tCompany',
     'Company\t',
     '\nCompany',
     'Company\n',
     '\rCompany',
     'Company\r',
     'Com\npany',
     'Com\tpany',
     'C\rom\npa\tny',
     'Company\tABC',
     ])
def test_invalid_pattern(xml, text):
    xml.manufacturer(text)
    xml.raises('not accepted by the pattern')


@pytest.mark.parametrize('occurances', [0, 2, 3, 10])
def test_one_occurance(xml, occurances):
    xml.manufacturer(occurances)
    xml.raises('model')  # <model> must be after <manufacturer>


def test_no_attributes(xml):
    xml.manufacturer('Hewlett Packard', foo='bar')
    xml.raises("attribute 'foo' is not allowed")
