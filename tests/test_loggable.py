import pytest


@pytest.mark.parametrize('text', ['0', 'false', '1', 'true'])
def test_valid_value(xml, text):
    xml.loggable(text)
    assert xml.is_valid()


@pytest.mark.parametrize('text', ['', 'False', 'True', 'anything', 'NULL', 'None'])
def test_invalid_value(xml, text):
    xml.loggable(text)
    xml.raises(r"atomic type 'xs:boolean'")


@pytest.mark.parametrize('occurances', [0, 2, 3, 10])
def test_one_occurance(xml, occurances):
    xml.loggable(occurances)
    xml.raises('traceable')  # <traceable> must be after <loggable>


def test_no_attributes(xml):
    xml.loggable('true', foo='bar')
    xml.raises("loggable', attribute 'foo'")
