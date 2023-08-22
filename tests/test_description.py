import pytest


@pytest.mark.parametrize(
    'text',
    ['', ' ', '\t', '0123ABC', '  hello\nworl\td ', '-,.{}!=-+()*^%$#@!;:'])
def test_valid_pattern(xml, text):
    xml.description(text)
    assert xml.is_valid()


@pytest.mark.parametrize('occurances', [0, 2, 3, 10])
def test_one_occurance(xml, occurances):
    xml.description(occurances)
    xml.raises('active')  # <active> must be after <description>


def test_no_attributes(xml):
    xml.description('A 6.5 digit digital multimeter', foo='bar')
    xml.raises("attribute 'foo' is not allowed")
