import pytest


@pytest.mark.parametrize(
    'text',
    ['0123ABC',
     '0123-ABC',
     '01 23A BC',
     '3m',
     'm3',
     '-,.{}!=-+()*^%$#@!;:',
     'Serial (\u00B0C)',
     's-(°C)',
     '0',
     '- a b {c} def, g .h @i',
     ])
def test_valid_pattern(xml, text):
    xml.serial(text)
    assert xml.is_valid()


@pytest.mark.parametrize(
    'text',
    ['',
     ' ',
     'b ',
     ' 0',
     '\t0',
     'a\n',
     '     ',
     '\t',
     '\n',
     '\r',
     '\n\r',
     '\n\n\n\n',
     '\t\t\t\t\t',
     ' \t\n',
     '   000001',
     'serial   ',
     '\tserial',
     'Serial\t',
     '\nSerial',
     '987\n',
     '\r123',
     '24-a\r',
     'abc\n01',
     'ab0\txz',
     'a\r9\n2\t3s',
     '9a2\tser',
     'A     B',
     'A  Bcd e',
     ])
def test_invalid_pattern(xml, text):
    xml.serial(text)
    xml.raises('not accepted by the pattern')


@pytest.mark.parametrize('occurances', [0, 2, 3, 10])
def test_one_occurance(xml, occurances):
    xml.serial(occurances)
    xml.raises('description')  # <description> must be after <serial>


def test_no_attributes(xml):
    xml.serial('87349862nf3287h', foo='bar')
    xml.raises("attribute 'foo' is not allowed")
