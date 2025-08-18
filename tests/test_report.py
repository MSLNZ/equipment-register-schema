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
    r = ('<report id="any" enteredBy="Joseph Borbely">'
         '  <anything/>'
         '</report>')
    xml.calibrations(xml.measurand(xml.component(r)))
    xml.raises(r'Expected is .*reportIssueDate')


def test_no_start_date(xml):
    r = ('<report id="any" enteredBy="Joseph Borbely">'
         '  <reportIssueDate>2024-06-25</reportIssueDate>'
         '  <anything/>'
         '</report>')
    xml.calibrations(xml.measurand(xml.component(r)))
    xml.raises(r'Expected is .*measurementStartDate')


def test_no_stop_date(xml):
    r = ('<report id="any" enteredBy="Joseph Borbely">'
         '  <reportIssueDate>2024-06-25</reportIssueDate>'
         '  <measurementStartDate>2000-01-01</measurementStartDate>'
         '  <anything/>'
         '</report>')
    xml.calibrations(xml.measurand(xml.component(r)))
    xml.raises(r'Expected is .*measurementStopDate')


def test_no_issuing_lab(xml):
    r = ('<report id="any" enteredBy="Joseph Borbely">'
         '  <reportIssueDate>2024-06-25</reportIssueDate>'
         '  <measurementStartDate>2000-01-01</measurementStartDate>'
         '  <measurementStopDate>2000-01-01</measurementStopDate>'
         '</report>')
    xml.calibrations(xml.measurand(xml.component(r)))
    xml.raises(r'Expected is .*issuingLaboratory')


def test_no_technical_procedure(xml):
    r = ('<report id="any" enteredBy="Joseph Borbely">'
         '  <reportIssueDate>2024-06-25</reportIssueDate>'
         '  <measurementStartDate>2000-01-01</measurementStartDate>'
         '  <measurementStopDate>2000-01-01</measurementStopDate>'
         '  <issuingLaboratory>MSL</issuingLaboratory>'
         '</report>')
    xml.calibrations(xml.measurand(xml.component(r)))
    xml.raises(r'Expected is .*technicalProcedure')


def test_no_conditions(xml):
    r = ('<report id="any" enteredBy="Joseph Borbely">'
         '  <reportIssueDate>2024-06-25</reportIssueDate>'
         '  <measurementStartDate>2000-01-01</measurementStartDate>'
         '  <measurementStopDate>2000-01-01</measurementStopDate>'
         '  <issuingLaboratory>MSL</issuingLaboratory>'
         '  <technicalProcedure/>'
         '</report>')
    xml.calibrations(xml.measurand(xml.component(r)))
    xml.raises(r'Expected is .*conditions')


def test_no_acceptance_criteria(xml):
    r = ('<report id="any" enteredBy="Joseph Borbely">'
         '  <reportIssueDate>2024-06-25</reportIssueDate>'
         '  <measurementStartDate>2000-01-01</measurementStartDate>'
         '  <measurementStopDate>2000-01-01</measurementStopDate>'
         '  <issuingLaboratory>MSL</issuingLaboratory>'
         '  <technicalProcedure/>'
         '  <conditions/>'
         '</report>')
    xml.calibrations(xml.measurand(xml.component(r)))
    xml.raises(r'Expected is .*acceptanceCriteria')


@pytest.mark.parametrize(
    ('text', 'attribs'),
    [('', {'hot': 'true'}),
     ('<anything/>', {}),
     ('<fruit colour="red" shape="round">apple</fruit>', {'x': '1', 'hello': 'world', 'stem': 'true'}),
     ('<min>10</min><max>70</max><unit>C</unit>', {}),
     ])
def test_acceptance_criteria(xml, text, attribs):
    ac = xml.element('acceptanceCriteria', text=text, **attribs)
    xml.calibrations(xml.measurand(xml.component(xml.report(acceptance_criteria=f'{ac}\n'))))
    assert xml.is_valid()


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
def test_conditions(xml, text, attribs):
    conditions = xml.element('conditions', text=text, **attribs)
    xml.calibrations(xml.measurand(xml.component(xml.report(conditions=conditions))))
    assert xml.is_valid()


def test_no_choice(xml):
    r = ('<report id="any" enteredBy="Joseph Borbely">'
         '  <reportIssueDate>2024-06-25</reportIssueDate>'
         '  <measurementStartDate>2000-01-01</measurementStartDate>'
         '  <measurementStopDate>2000-01-01</measurementStopDate>'
         '  <issuingLaboratory>MSL</issuingLaboratory>'
         '  <technicalProcedure/>'
         '  <conditions/>'
         '  <acceptanceCriteria/>'
         '</report>')
    xml.calibrations(xml.measurand(xml.component(r)))
    xml.raises(r'Expected is one of .*equation, .*file, .*serialised, .*table')


def test_invalid_choice(xml):
    xml.calibrations(xml.measurand(xml.component(xml.report(choice='<invalid/>'))))
    xml.raises(r'Expected is one of .*equation, .*file, .*serialised, .*table')


def test_unexpected_element(xml):
    xml.calibrations(xml.measurand(xml.component(xml.report(extra='<extra/>'))))
    xml.raises(r"extra': This element is not expected")


def test_multiple_choices_valid(xml):
    table = xml.table()

    serialised = ('<serialised>'
                  '  <gtcArchiveJSON>{}</gtcArchiveJSON>'
                  '</serialised>')

    file = (f'<file>'
            f'  <url>file.txt</url>'
            f'  <sha256>{xml.SHA256}</sha256>'
            f'</file>')

    equation = ('<equation>'
                '  <value variables="x">2*x</value>'
                '  <uncertainty variables="">1.0</uncertainty>'
                '  <unit>m</unit>'
                '  <ranges/>'
                '</equation>')

    cvd = ('<cvdCoefficients>'
           '  <R0>100</R0>'
           '  <A>1</A>'
           '  <B>1</B>'
           '  <C>1</C>'
           '  <D>1</D>'
           '  <uncertainty variables="">0.2</uncertainty>'
           '  <range><minimum>0</minimum><maximum>100</maximum></range>'
           '</cvdCoefficients>')

    r = (f'<report id="any" enteredBy="Joseph Borbely">'
         f'  <reportIssueDate>2024-06-25</reportIssueDate>'
         f'  <measurementStartDate>2000-01-01</measurementStartDate>'
         f'  <measurementStopDate>2000-01-01</measurementStopDate>'
         f'  <issuingLaboratory>MSL</issuingLaboratory>'
         f'  <technicalProcedure/>'
         f'  <conditions/>'
         f'  <acceptanceCriteria/>'
         f'  {file}'
         f'  {table}'
         f'  {cvd}'
         f'  {equation}'
         f'  {equation}'
         f'  {cvd}'
         f'  {serialised}'
         f'  {table}'
         f'  {file}'
         f'  {equation}'
         f'  {cvd}'
         f'  {cvd}'
         f'  {file}'
         f'  {serialised}'
         f'  {serialised}'
         f'  {cvd}'
         f'</report>')
    xml.calibrations(xml.measurand(xml.component(r)))
    assert xml.is_valid()


def test_multiple_choices_one_invalid(xml):
    table = xml.table()

    serialised = ('<serialised>'
                  '  <gtcArchiveJSON>{}</gtcArchiveJSON>'
                  '</serialised>')

    file = (f'<file>'
            f'  <url>file.txt</url>'
            f'  <sha256>{xml.SHA256}</sha256>'
            f'</file>')

    equation = ('<equation>'
                '  <value variables="x">2*x</value>'
                '  <uncertainty variables="">1.0</uncertainty>'
                '  <unit>m</unit>'
                '  <ranges/>'
                '</equation>')

    cvd = ('<cvdCoefficients>'
           '  <R0>100</R0>'
           '  <A>1</A>'
           '  <B>1</B>'
           '  <C>1</C>'
           '  <D>1</D>'
           '  <uncertainty variables="">0.2</uncertainty>'
           '  <range><minimum>0</minimum><maximum>100</maximum></range>'
           '</cvdCoefficients>')

    r = (f'<report id="any" enteredBy="Joseph Borbely">'
         f'  <reportIssueDate>2024-06-25</reportIssueDate>'
         f'  <measurementStartDate>2000-01-01</measurementStartDate>'
         f'  <measurementStopDate>2000-01-01</measurementStopDate>'
         f'  <issuingLaboratory>MSL</issuingLaboratory>'
         f'  <technicalProcedure/>'
         f'  <conditions/>'
         f'  <acceptanceCriteria/>'
         f'  {file}'
         f'  {table}'
         f'  {serialised}'
         f'  {cvd}'
         f'  <apple>red</apple>'
         f'  {equation}'
         f'</report>')
    xml.calibrations(xml.measurand(xml.component(r)))
    xml.raises(r"apple': This element is not expected")


def test_multiple_choices_unexpected_element_interleaved(xml):
    table = xml.table()
    r = (f'<report id="any" enteredBy="Joseph Borbely">'
         f'  <reportIssueDate>2024-06-25</reportIssueDate>'
         f'  <measurementStartDate>2000-01-01</measurementStartDate>'
         f'  <measurementStopDate>2000-01-01</measurementStopDate>'
         f'  <issuingLaboratory>MSL</issuingLaboratory>'
         f'  <technicalProcedure/>'
         f'  <conditions/>'
         f'  <acceptanceCriteria/>'
         f'  {table}'
         f'  <extra><name>value</name></extra>'
         f'  {table}'
         f'</report>')
    xml.calibrations(xml.measurand(xml.component(r)))
    xml.raises(r"extra': This element is not expected")


@pytest.mark.parametrize('name', ['', '    '])
def test_entered_by_empty_string(xml, name):
    xml.calibrations(xml.measurand(xml.component(xml.report(entered_by=name))))
    xml.raises('not an element of the set')


@pytest.mark.parametrize('name', ['Tom Stewart', 'Hamish Edgar', 'Ellie Molloy'])
def test_checked_by_valid(xml, name):
    r = (f'<report id="any" enteredBy="Joseph Borbely" checkedBy="{name}">'
         f'  <reportIssueDate>2024-06-25</reportIssueDate>'
         f'  <measurementStartDate>2000-01-01</measurementStartDate>'
         f'  <measurementStopDate>2000-01-01</measurementStopDate>'
         f'  <issuingLaboratory>MSL</issuingLaboratory>'
         f'  <technicalProcedure/>'
         f'  <conditions/>'
         f'  <acceptanceCriteria/>'
         f'  {xml.table()}'
         f'</report>')
    xml.calibrations(xml.measurand(xml.component(r)))
    assert xml.is_valid()


@pytest.mark.parametrize('name', ['Tim Stewart', 'Hamish   Edgar', ' Ellie Molloy'])
def test_checked_by_invalid(xml, name):
    r = (f'<report id="any" enteredBy="Joseph Borbely" checkedBy="{name}">'
         f'  <reportIssueDate>2024-06-25</reportIssueDate>'
         f'  <measurementStartDate>2000-01-01</measurementStartDate>'
         f'  <measurementStopDate>2000-01-01</measurementStopDate>'
         f'  <issuingLaboratory>MSL</issuingLaboratory>'
         f'  <technicalProcedure/>'
         f'  <conditions/>'
         f'  <acceptanceCriteria/>'
         f'  {xml.table()}'
         f'</report>')
    xml.calibrations(xml.measurand(xml.component(r)))
    xml.raises("not an element of the set")


def test_checked_date_valid(xml):
    r = (f'<report id="any" enteredBy="Joseph Borbely" checkedBy="Joseph Borbely" checkedDate="2025-08-06">'
         f'  <reportIssueDate>2024-06-25</reportIssueDate>'
         f'  <measurementStartDate>2000-01-01</measurementStartDate>'
         f'  <measurementStopDate>2000-01-01</measurementStopDate>'
         f'  <issuingLaboratory>MSL</issuingLaboratory>'
         f'  <technicalProcedure/>'
         f'  <conditions/>'
         f'  <acceptanceCriteria/>'
         f'  {xml.table()}'
         f'</report>')
    xml.calibrations(xml.measurand(xml.component(r)))
    assert xml.is_valid()


def test_checked_date_invalid(xml):
    r = '<report id="any" enteredBy="Joseph Borbely" checkedBy="Joseph Borbely" checkedDate="06-2025-08" />'
    xml.calibrations(xml.measurand(xml.component(r)))
    xml.raises('not a valid value')
