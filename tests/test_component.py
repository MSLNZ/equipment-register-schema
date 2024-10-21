import pytest


def test_default(xml):
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


def test_no_name_attribute(xml):
    xml.calibrations(xml.measurand('<component/>'))
    xml.raises(r"attribute 'name' is required but missing")


def test_report_invalid_element_name(xml):
    xml.calibrations(xml.measurand(xml.component('<anything/>')))
    xml.raises(r'Expected is .*report')


def test_report_no_content(xml):
    xml.calibrations(xml.measurand(xml.component('<report id="anything"/>')))
    xml.raises(r'Expected is .*reportIssueDate')


def test_report_no_id(xml):
    xml.calibrations(xml.measurand(xml.component('<report/>')))
    xml.raises("The attribute 'id' is required but missing")


@pytest.mark.parametrize(
    'identity',
    ['',
     ' ',
     '     ',
     '\t',
     '\n',
     '\r',
     '\n\r',
     '\n\n\n\n',
     '\n \n \n  \n ',
     '\t\t\t\t\t',
     ' \t\n',
     ])
def test_report_invalid_id(xml, identity):
    xml.calibrations(xml.measurand(xml.component(f'<report id="{identity}"/>')))
    xml.raises('not accepted by the pattern')
