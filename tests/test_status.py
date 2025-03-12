import pytest


@pytest.mark.parametrize(
    'text',
    ['Active',
     'Damaged',
     'Dormant',
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


@pytest.mark.parametrize('occurrences', [0, 2, 3, 10])
def test_one_occurrence(xml, occurrences):
    xml.status(occurrences)
    xml.raises('loggable')  # <loggable> must be after <status>


def test_no_attributes(xml):
    xml.status('Active', foo='bar')
    xml.raises("status', attribute 'foo'")
