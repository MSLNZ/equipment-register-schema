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
    xml.calibrations(xml.measurand(xml.component('<report id="anything" enteredBy="Joseph Borbely"/>')))
    xml.raises(r'Expected is .*reportIssueDate')


def test_report_no_id(xml):
    xml.calibrations(xml.measurand(xml.component('<report/>')))
    xml.raises("The attribute 'id' is required but missing")


def test_report_no_entered_by(xml):
    xml.calibrations(xml.measurand(xml.component('<report id="x"/>')))
    xml.raises("The attribute 'enteredBy' is required but missing")


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


def test_multiple_choices(xml):
    a = '<adjustment date="2024-10-17">Cleaned the filter</adjustment>'
    r = xml.report()
    d = xml.digital_report()
    p = xml.performance_check()
    final = f'{a}{r}{a}{d}{d}{p}{r}{p}{r}{r}{r}{a}{a}{d}{p}{p}'
    xml.calibrations(xml.measurand(xml.component(final)))
    assert xml.is_valid()
