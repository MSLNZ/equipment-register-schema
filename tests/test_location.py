import pytest


@pytest.mark.parametrize(
    'text',
    ['General',
     'Photometric Bench',
     'Spectrophotometer',
     'Detector Responsivity',
     'Cryogenic Radiometer',
     'Goniospectrophotometer',
     'Single Photon',
     'Flexible Optics',
     ])
def test_valid_enum(xml, text):
    xml.location(text)
    assert xml.is_valid()


@pytest.mark.parametrize(
    'lab',
    ['',
     ' ',
     '\n',
     '\t',
     '\r',
     '   \t \r  \n',
     'MSL',
     ' General',
     'General ',
     'Photometric\tBench',
     'Spectrophotometer\n',
     'Does not exist',
     ])
def test_invalid_enum(xml, lab):
    xml.location(lab)
    xml.raises("not an element of the set")


@pytest.mark.parametrize('occurances', [0, 2, 3, 10])
def test_one_occurance(xml, occurances):
    xml.location(occurances)
    xml.raises('status')  # <status> must be after <location>


def test_no_attributes(xml):
    xml.location('General', foo='bar')
    xml.raises("attribute 'foo' is not allowed")
