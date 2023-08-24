import pytest


@pytest.mark.parametrize(
    'text',
    ['Model',
     'Model A',
     'Model, ABC.',
     '3m',
     'm3',
     '-,.{}!=-+()*^%$#@!;:',
     'Model (\u00B0C)',
     'Model (°C)',
     'a',
     '- a b {c} def, g .h @i',
     ])
def test_valid_pattern(xml, text):
    xml.model(text)
    assert xml.is_valid()


@pytest.mark.parametrize(
    'text',
    ['',
     ' ',
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
     '   Model',
     'Model   ',
     '\tModel',
     'Model\t',
     '\nModel',
     'Model\n',
     '\rModel',
     'Model\r',
     'Mod\nel',
     'Mod\tel',
     'M\ro\nd\tel',
     'Model\tABC',
     'A     B',
     'A  Bcd e',
     ])
def test_invalid_pattern(xml, text):
    xml.model(text)
    xml.raises('not accepted by the pattern')


@pytest.mark.parametrize('occurances', [0, 2, 3, 10])
def test_one_occurance(xml, occurances):
    xml.model(occurances)
    xml.raises('serial')  # <serial> must be after <model>


def test_no_attributes(xml):
    xml.model('34401a', foo='bar')
    xml.raises("attribute 'foo' is not allowed")
