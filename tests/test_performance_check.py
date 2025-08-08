import pytest

from tests.conftest import (
    INVALID_DATES,
    VALID_TECHNICAL_PROCEDURES,
    INVALID_TECHNICAL_PROCEDURES,
)

INVALID_PERSON_NAME = [
    '',
    ' ',
    '       ',
    '\t',
    '\t         ',
    '\r',
    '\n',
    ' \t\n \r ',
    'First\nLast',
    'First\rLast',
    'First Last\r',
    'First Last\r\n',
    '\nFirst Last',
]

VALID_PERSON_NAME = [
    'a',
    ' a',
    'a ',
    '  a     ',
    'First X. Last',
    '   First Last',
    '   F i r s    t           L a s t   ~-_=+)(*^%$#!',
]


def test_default(xml):
    check = xml.performance_check()
    xml.calibrations(xml.measurand(xml.component(check)))
    assert xml.is_valid()


def test_date_missing(xml):
    check = '<performanceCheck/>'
    xml.calibrations(xml.measurand(xml.component(check)))
    xml.raises(r"attribute 'completedDate' is required but missing")


@pytest.mark.parametrize(
    'attribs',
    [
        {'apple': 'red'},
        {'completedDate': '2024-12-18', 'apple': 'red'},
    ])
def test_attribute_invalid(xml, attribs):
    check = xml.performance_check(**attribs)
    xml.calibrations(xml.measurand(xml.component(check)))
    xml.raises(r"attribute 'apple' is not allowed")


@pytest.mark.parametrize('date', INVALID_DATES)
def test_date_invalid(xml, date):
    check = xml.performance_check(date=date)
    xml.calibrations(xml.measurand(xml.component(check)))
    xml.raises(r'not a valid value of the atomic type')


@pytest.mark.parametrize('date', ['1999-12-19', '2100-01-01'])
def test_date_valid(xml, date):
    check = xml.performance_check(date=date)
    xml.calibrations(xml.measurand(xml.component(check)))
    assert xml.is_valid()


def test_empty(xml):
    check = '<performanceCheck completedDate="2024-12-18" enteredBy="Joseph Borbely"/>'
    xml.calibrations(xml.measurand(xml.component(check)))
    xml.raises(r'Expected is .*competency')


def test_competency_missing(xml):
    check = xml.performance_check(competency=None)
    xml.calibrations(xml.measurand(xml.component(check)))
    xml.raises(r'Expected is .*competency')


def test_competency_empty(xml):
    check = ('<performanceCheck completedDate="2024-12-18" enteredBy="Joseph Borbely">'
             '  <competency/>'
             '</performanceCheck>')
    xml.calibrations(xml.measurand(xml.component(check)))
    xml.raises(r'Expected is .*worker')


def test_competency_unexpected_child(xml):
    check = ('<performanceCheck completedDate="2024-12-18" enteredBy="Joseph Borbely">'
             '  <competency>'
             '    <unexpected/>'
             '  </competency>'
             '</performanceCheck>')
    xml.calibrations(xml.measurand(xml.component(check)))
    xml.raises(r'Expected is .*worker')


def test_worker_missing(xml):
    check = ('<performanceCheck completedDate="2024-12-18" enteredBy="Joseph Borbely">'
             '  <competency>'
             '    <checker>MSL</checker>'
             '    <technicalProcedure>MSLT.E.0</technicalProcedure>'
             '  </competency>'
             '</performanceCheck>')
    xml.calibrations(xml.measurand(xml.component(check)))
    xml.raises(r'Expected is .*worker')


def test_checker_missing(xml):
    check = ('<performanceCheck completedDate="2024-12-18" enteredBy="Joseph Borbely">'
             '  <competency>'
             '    <worker>MSL</worker>'
             '    <technicalProcedure>MSLT.E.0</technicalProcedure>'
             '  </competency>'
             '</performanceCheck>')
    xml.calibrations(xml.measurand(xml.component(check)))
    xml.raises(r'Expected is .*checker')


def test_technical_procedure_missing(xml):
    check = ('<performanceCheck completedDate="2024-12-18" enteredBy="Joseph Borbely">'
             '  <competency>'
             '    <worker>MSL</worker>'
             '    <checker>MSL</checker>'
             '  </competency>'
             '</performanceCheck>')
    xml.calibrations(xml.measurand(xml.component(check)))
    xml.raises(r'Expected is .*technicalProcedure')


def test_competency_extra_child(xml):
    check = ('<performanceCheck completedDate="2024-12-18" enteredBy="Joseph Borbely">'
             '  <competency>'
             '    <worker>MSL</worker>'
             '    <checker>MSL</checker>'
             '    <technicalProcedure>MSLT.E.0</technicalProcedure>'
             '    <extra>MSL</extra>'
             '  </competency>'
             '</performanceCheck>')
    xml.calibrations(xml.measurand(xml.component(check)))
    xml.raises(r"extra': This element is not expected")


def test_conditions_missing(xml):
    check = xml.performance_check(conditions=None)
    xml.calibrations(xml.measurand(xml.component(check)))
    xml.raises(r'Expected is .*conditions')


def test_choice_missing(xml):
    check = xml.performance_check(choice='')
    xml.calibrations(xml.measurand(xml.component(check)))
    xml.raises(r'Expected is one of .*equation, .*file, .*serialised, .*table')


def test_multiple_choices(xml):
    t = xml.table()

    s = ('<serialised>'
         '  <gtcArchiveJSON>{}</gtcArchiveJSON>'
         '</serialised>')

    f = (f'<file>'
         f'  <url>file.txt</url>'
         f'  <sha256>{xml.SHA256}</sha256>'
         f'</file>')

    e = ('<equation>'
         '  <value variables="x">2*x</value>'
         '  <uncertainty variables="">1.0</uncertainty>'
         '  <unit>m</unit>'
         '  <ranges/>'
         '</equation>')

    c = ('<cvdCoefficients>'
        '  <R0>100</R0>'
        '  <A>1</A>'
        '  <B>1</B>'
        '  <C>1</C>'
        '  <uncertainty variables="">0.2</uncertainty>'
        '  <range><minimum>0</minimum><maximum>100</maximum></range>'
        '</cvdCoefficients>')

    choice = f'{t}{e}{c}{f}{s}{t}{t}{t}{c}{s}{s}{f}{e}{e}{f}{e}{s}{s}{f}{t}{t}{c}'
    check = xml.performance_check(choice=choice)
    xml.calibrations(xml.measurand(xml.component(check)))
    assert xml.is_valid()


def test_unexpected(xml):
    check = xml.performance_check(extra='<another/>')
    xml.calibrations(xml.measurand(xml.component(check)))
    xml.raises(r"another': This element is not expected")


@pytest.mark.parametrize(
    ('text', 'attribs'),
    [('', {'hot': 'true'}),
     ('<anything/>', {}),
     ('<fruit colour="red" shape="round">apple</fruit>', {'x': '1', 'hello': 'world', 'stem': 'true'}),
     ('<min>10</min><max>70</max><unit>C</unit>', {}),
     ])
def test_conditions(xml, text, attribs):
    conditions = xml.element('conditions', text=text, **attribs)
    check = xml.performance_check(conditions=conditions)
    xml.calibrations(xml.measurand(xml.component(check)))
    assert xml.is_valid()


@pytest.mark.parametrize('name', INVALID_PERSON_NAME)
def test_worker_invalid(xml, name):
    check = xml.performance_check(worker=name)
    xml.calibrations(xml.measurand(xml.component(check)))
    xml.raises(r'not accepted by the pattern')


@pytest.mark.parametrize('name', VALID_PERSON_NAME)
def test_worker_valid(xml, name):
    check = xml.performance_check(worker=name)
    xml.calibrations(xml.measurand(xml.component(check)))
    assert xml.is_valid()


@pytest.mark.parametrize('name', INVALID_PERSON_NAME)
def test_checker_invalid(xml, name):
    check = xml.performance_check(checker=name)
    xml.calibrations(xml.measurand(xml.component(check)))
    xml.raises(r'not accepted by the pattern')


@pytest.mark.parametrize('name', VALID_PERSON_NAME)
def test_checker_valid(xml, name):
    check = xml.performance_check(checker=name)
    xml.calibrations(xml.measurand(xml.component(check)))
    assert xml.is_valid()


@pytest.mark.parametrize('value', INVALID_TECHNICAL_PROCEDURES)
def test_technical_procedure_invalid(xml, value):
    check = xml.performance_check(technical_procedure=value)
    xml.calibrations(xml.measurand(xml.component(check)))
    xml.raises(r'not accepted by the pattern')


@pytest.mark.parametrize('value', VALID_TECHNICAL_PROCEDURES)
def test_technical_procedure_valid(xml, value):
    check = xml.performance_check(technical_procedure=value)
    xml.calibrations(xml.measurand(xml.component(check)))
    assert xml.is_valid()


@pytest.mark.parametrize('name', ['', '    '])
def test_entered_by_empty_string(xml, name):
    check = xml.performance_check(entered_by=name)
    xml.calibrations(xml.measurand(xml.component(check)))
    xml.raises('not an element of the set')


@pytest.mark.parametrize('name', ['Lenice Evergreen', 'Blair Hall', 'Yang Yenn Tan'])
def test_checked_by_valid(xml, name):
    check = xml.performance_check(completedDate="2025-08-05", enteredBy="Joseph Borbely", checkedBy=name)
    xml.calibrations(xml.measurand(xml.component(check)))
    assert xml.is_valid()


@pytest.mark.parametrize('name', ['Larry Evergreen', ' Blair Hall', 'Yang Yenn Tan '])
def test_checked_by_invalid(xml, name):
    check = xml.performance_check(completedDate="2025-08-05", enteredBy="Joseph Borbely", checkedBy=name)
    xml.calibrations(xml.measurand(xml.component(check)))
    xml.raises('not an element of the set')


def test_checked_date_valid(xml):
    check = xml.performance_check(completedDate="2025-08-05", enteredBy="Joseph Borbely", checkedDate="2025-08-06")
    xml.calibrations(xml.measurand(xml.component(check)))
    assert xml.is_valid()


def test_checked_date_invalid(xml):
    check = xml.performance_check(completedDate="2025-08-05", enteredBy="Joseph Borbely", checkedDate="06-2025-08")
    xml.calibrations(xml.measurand(xml.component(check)))
    xml.raises('not a valid value')
