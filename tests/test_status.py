import pytest


@pytest.mark.parametrize(
    'text',
    ['Active',
     'Damaged',
     'Retired',
     ])
def test_valid_enum(xml, text):
    xml.status(text)
    assert xml.is_valid()


@pytest.mark.parametrize(
    'text',
    ['',
     ' ',
     '\n',
     '\t',
     '\r',
     '   \t \r  \n',
     'MSL',
     ' Active',
     'Damaged ',
     'Retired\n',
     'Does not exist',
     ])
def test_invalid_enum(xml, text):
    xml.status(text)
    xml.raises("not an element of the set")


@pytest.mark.parametrize('occurances', [0, 2, 3, 10])
def test_one_occurance(xml, occurances):
    xml.status(occurances)
    xml.raises('active')  # <active> must be after <status>


def test_no_attributes(xml):
    xml.status('Active', foo='bar')
    xml.raises("attribute 'foo' is not allowed")
