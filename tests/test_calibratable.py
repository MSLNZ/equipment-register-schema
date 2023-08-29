import pytest


@pytest.mark.parametrize('text', ['0', 'false', '1', 'true'])
def test_valid_value(xml, text):
    xml.calibratable(text)
    assert xml.is_valid()


@pytest.mark.parametrize('text', ['', 'False', 'True', 'anything', 'NULL', 'None'])
def test_invalid_value(xml, text):
    xml.calibratable(text)
    xml.raises(r"atomic type 'xs:boolean'")


@pytest.mark.parametrize('occurances', [0, 2, 3, 10])
def test_one_occurance(xml, occurances):
    xml.calibratable(occurances)
    xml.raises('calibrations')  # <calibrations> must be after <calibratable>


def test_no_attributes(xml):
    xml.calibratable('true', foo='bar')
    xml.raises("attribute 'foo' is not allowed")
