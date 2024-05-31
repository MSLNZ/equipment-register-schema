import pytest

from tests.conftest import INVALID_DATES


@pytest.mark.parametrize(
    'attribs',
    [{'foo': '2023-01-01'},
     {'date': '2023-01-01', 'foo': '2023-01-01'},
     ])
def test_invalid_attribute_name(xml, attribs):
    xml.calibrations(xml.measurand(xml.component(xml.report(**attribs))))
    xml.raises(r"report', attribute 'foo'")


@pytest.mark.parametrize('value', INVALID_DATES)
def test_invalid_attribute_value(xml, value):
    xml.calibrations(xml.measurand(xml.component(xml.report(date=value))))
    xml.raises(rf"report', attribute 'date': '{value}' is not a valid value")


@pytest.mark.parametrize(
    'value',
    ['',
     ' ',
     'i\n',
     '     ',
     '\t',
     '\n',
     '\r',
     '\n\r',
     '\n\n\n\n',
     '\t\t\t\t\t',
     ' \t\n',
     '\nIdentity',
     'Identity\n',
     '\rIdentity',
     'Identity\r',
     'Iden\ntity',
     'I\rde\nti\ty',
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
def test_invalid_start_value(xml, value):
    xml.calibrations(xml.measurand(xml.component(xml.report(start=value))))
    xml.raises(f"startDate': '{value}' is not a valid value")


@pytest.mark.parametrize('value', INVALID_DATES)
def test_invalid_stop_value(xml, value):
    xml.calibrations(xml.measurand(xml.component(xml.report(stop=value))))
    xml.raises(f"stopDate': '{value}' is not a valid value")


def test_no_number(xml):
    r = '<report><anything/></report>'
    xml.calibrations(xml.measurand(xml.component(r)))
    xml.raises(r'Expected is .*number')


def test_no_start_date(xml):
    r = ('<report>'
         '  <number>any</number>'
         '  <anything/>'
         '</report>')
    xml.calibrations(xml.measurand(xml.component(r)))
    xml.raises(r'Expected is .*startDate')


def test_no_stop_date(xml):
    r = ('<report>'
         '  <number>any</number>'
         '  <startDate>2000-01-01</startDate>'
         '  <anything/>'
         '</report>')
    xml.calibrations(xml.measurand(xml.component(r)))
    xml.raises(r'Expected is .*stopDate')


def test_no_criteria(xml):
    r = ('<report>'
         '  <number>any</number>'
         '  <startDate>2000-01-01</startDate>'
         '  <stopDate>2000-01-01</stopDate>'
         '</report>')
    xml.calibrations(xml.measurand(xml.component(r)))
    xml.raises(r'Expected is .*criteria')


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
    r = ('<report>'
         '  <number>any</number>'
         '  <startDate>2000-01-01</startDate>'
         '  <stopDate>2000-01-01</stopDate>'
         '  <criteria/>'
         '</report>')
    xml.calibrations(xml.measurand(xml.component(r)))
    xml.raises(r'Expected is one of .*equation, .*file, .*gtcArchive, .*table')


def test_invalid_choice(xml):
    xml.calibrations(xml.measurand(xml.component(xml.report(choice='<invalid/>'))))
    xml.raises(r'Expected is one of .*equation, .*file, .*gtcArchive, .*table')
