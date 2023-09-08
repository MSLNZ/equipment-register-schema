import pytest


def test_empty(xml):
    xml.calibrations(xml.measurand(xml.component()))
    assert xml.is_valid()


@pytest.mark.parametrize(
    'attribs',
    [{'foo': 'bar'},
     {'name': 'Ch1', 'foo': 'bar'},
     ])
def test_invalid_attribute(xml, attribs):
    xml.calibrations(xml.measurand(xml.component(**attribs)))
    xml.raises(r"component', attribute 'foo'")


def test_subelement_invalid_name(xml):
    xml.calibrations(xml.measurand(xml.component('<anything/>')))
    xml.raises(r'Expected is .*report')


def test_subelement_invalid_content(xml):
    xml.calibrations(xml.measurand(xml.component('<report/>')))
    xml.raises(r'Expected is .*id')
