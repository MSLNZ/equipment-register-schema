import pytest

from tests.conftest import INVALID_DATES


def test_no_attributes_allowed(xml):
    xml.calibrations(xml.measurand(xml.component(xml.report(date='2023-01-01'))))
    xml.raises(r"report', attribute 'date'")


@pytest.mark.parametrize(
    'value',
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
def test_invalid_number_value(xml, value):
    xml.calibrations(xml.measurand(xml.component(xml.report(number=value))))
    xml.raises('not accepted by the pattern')


@pytest.mark.parametrize(
    'value',
    ['   a   b   c ',
     'Radiometry/2023/123',
     'PTB 44183/12',
     '#987654-08',
     ])
def test_valid_number_value(xml, value):
    xml.calibrations(xml.measurand(xml.component(xml.report(number=value))))
    assert xml.is_valid()


@pytest.mark.parametrize('value', INVALID_DATES)
def test_invalid_issue_date(xml, value):
    xml.calibrations(xml.measurand(xml.component(xml.report(issue=value))))
    xml.raises(f"reportIssueDate': '{value}' is not a valid value")


@pytest.mark.parametrize('value', INVALID_DATES)
def test_invalid_start_value(xml, value):
    xml.calibrations(xml.measurand(xml.component(xml.report(start=value))))
    xml.raises(f"measurementStartDate': '{value}' is not a valid value")


@pytest.mark.parametrize('value', INVALID_DATES)
def test_invalid_stop_value(xml, value):
    xml.calibrations(xml.measurand(xml.component(xml.report(stop=value))))
    xml.raises(f"measurementStopDate': '{value}' is not a valid value")


@pytest.mark.parametrize('value', ['', '  ', '\r\n', '\nMSL\n'])
def test_invalid_issuing_lab(xml, value):
    xml.calibrations(xml.measurand(xml.component(xml.report(lab=value))))
    xml.raises(r'not accepted by the pattern')


@pytest.mark.parametrize('value', ['MSL', 'NMI-A', 'PTB', 'NIST', 'KRISS'])
def test_valid_issuing_lab(xml, value):
    xml.calibrations(xml.measurand(xml.component(xml.report(lab=value))))
    assert xml.is_valid()


def test_invalid_issuing_lab_attribute_name(xml):
    lab = '<issuingLaboratory contact="">MSL</issuingLaboratory>'
    xml.calibrations(xml.measurand(xml.component(xml.report(lab=lab))))
    xml.raises(r"attribute 'contact' is not allowed")


def test_extra_issuing_lab_attribute_name(xml):
    lab = '<issuingLaboratory person="Me" contact="">MSL</issuingLaboratory>'
    xml.calibrations(xml.measurand(xml.component(xml.report(lab=lab))))
    xml.raises(r"attribute 'contact' is not allowed")


@pytest.mark.parametrize('value', ['', '  ', '\t', '\r\n'])
def test_invalid_issuing_lab_attribute_value(xml, value):
    lab = f'<issuingLaboratory person="{value}">MSL</issuingLaboratory>'
    xml.calibrations(xml.measurand(xml.component(xml.report(lab=lab))))
    xml.raises(r'not accepted by the pattern')


@pytest.mark.parametrize('value', ['Name', 'First M. Last', 'name123@email.loc'])
def test_valid_issuing_lab_attribute_value(xml, value):
    lab = f'<issuingLaboratory person="{value}">MSL</issuingLaboratory>'
    xml.calibrations(xml.measurand(xml.component(xml.report(lab=lab))))
    assert xml.is_valid()


def test_no_number(xml):
    r = '<report><anything/></report>'
    xml.calibrations(xml.measurand(xml.component(r)))
    xml.raises("The attribute 'id' is required but missing")


def test_no_issue_date(xml):
    r = ('<report id="any">'
         '  <anything/>'
         '</report>')
    xml.calibrations(xml.measurand(xml.component(r)))
    xml.raises(r'Expected is .*reportIssueDate')


def test_no_start_date(xml):
    r = ('<report id="any">'
         '  <reportIssueDate>2024-06-25</reportIssueDate>'
         '  <anything/>'
         '</report>')
    xml.calibrations(xml.measurand(xml.component(r)))
    xml.raises(r'Expected is .*measurementStartDate')


def test_no_stop_date(xml):
    r = ('<report id="any">'
         '  <reportIssueDate>2024-06-25</reportIssueDate>'
         '  <measurementStartDate>2000-01-01</measurementStartDate>'
         '  <anything/>'
         '</report>')
    xml.calibrations(xml.measurand(xml.component(r)))
    xml.raises(r'Expected is .*measurementStopDate')


def test_no_issuing_lab(xml):
    r = ('<report id="any">'
         '  <reportIssueDate>2024-06-25</reportIssueDate>'
         '  <measurementStartDate>2000-01-01</measurementStartDate>'
         '  <measurementStopDate>2000-01-01</measurementStopDate>'
         '</report>')
    xml.calibrations(xml.measurand(xml.component(r)))
    xml.raises(r'Expected is .*issuingLaboratory')


def test_no_technical_procedure(xml):
    r = ('<report id="any">'
         '  <reportIssueDate>2024-06-25</reportIssueDate>'
         '  <measurementStartDate>2000-01-01</measurementStartDate>'
         '  <measurementStopDate>2000-01-01</measurementStopDate>'
         '  <issuingLaboratory>MSL</issuingLaboratory>'
         '</report>')
    xml.calibrations(xml.measurand(xml.component(r)))
    xml.raises(r'Expected is .*technicalProcedure')


def test_no_criteria(xml):
    r = ('<report id="any">'
         '  <reportIssueDate>2024-06-25</reportIssueDate>'
         '  <measurementStartDate>2000-01-01</measurementStartDate>'
         '  <measurementStopDate>2000-01-01</measurementStopDate>'
         '  <issuingLaboratory>MSL</issuingLaboratory>'
         '  <technicalProcedure/>'
         '</report>')
    xml.calibrations(xml.measurand(xml.component(r)))
    xml.raises(r'Expected is .*criteria')


@pytest.mark.parametrize(
    'method',
    ['',
     ' ',
     'MSLT.H.022.483'
     '\tanything \n numbers=1234567890 and \r\n\n symbols=~#$%^*(){}":_+-|?,./;[] \r\n'])
def test_technical_procedure(xml, method):
    xml.calibrations(xml.measurand(xml.component(xml.report(method=method))))
    assert xml.is_valid()


@pytest.mark.parametrize(
    ('text', 'attribs'),
    [('', {'hot': 'true'}),
     ('<anything/>', {}),
     ('<fruit colour="red" shape="round">apple</fruit>', {'x': '1', 'hello': 'world', 'stem': 'true'}),
     ('<min>10</min><max>70</max><unit>C</unit>', {}),
     ])
def test_criteria(xml, text, attribs):
    criteria = xml.element('criteria', text=text, **attribs)
    xml.calibrations(xml.measurand(xml.component(xml.report(criteria=criteria))))
    assert xml.is_valid()


def test_no_choice(xml):
    r = ('<report id="any">'
         '  <reportIssueDate>2024-06-25</reportIssueDate>'
         '  <measurementStartDate>2000-01-01</measurementStartDate>'
         '  <measurementStopDate>2000-01-01</measurementStopDate>'
         '  <issuingLaboratory>MSL</issuingLaboratory>'
         '  <technicalProcedure/>'
         '  <criteria/>'
         '</report>')
    xml.calibrations(xml.measurand(xml.component(r)))
    xml.raises(r'Expected is one of .*equation, .*file, .*serialised, .*table')


def test_invalid_choice(xml):
    xml.calibrations(xml.measurand(xml.component(xml.report(choice='<invalid/>'))))
    xml.raises(r'Expected is one of .*equation, .*file, .*serialised, .*table')


def test_extra_invalid_tag_name(xml):
    xml.calibrations(xml.measurand(xml.component(xml.report(extra='<invalid/>'))))
    xml.raises(r'Expected is .*extra')


@pytest.mark.parametrize(
    ('text', 'attribs'),
    [('', {'hot': 'true'}),
     ('<anything/>', {}),
     ('<fruit colour="red" shape="round">apple</fruit>', {'x': '1', 'hello': 'world', 'stem': 'true'}),
     ('<min>10</min><max>70</max><unit>C</unit>', {}),
     ])
def test_extra(xml, text, attribs):
    extra = xml.element('extra', text=text, **attribs)
    xml.calibrations(xml.measurand(xml.component(xml.report(extra=f'{extra}\n'))))
    assert xml.is_valid()
