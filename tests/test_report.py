import pytest


bad_dates = [
    '',
    '   ',
    '2023',
    '2023-05',
    '2023-24-05',
    '23-24-05',
    '05-24-2023',
    '24-05-2023',
    'text',
    '24 May 2023',
]


@pytest.mark.parametrize(
    'attribs',
    [{'foo': '2023-01-01'},
     {'date': '2023-01-01', 'foo': '2023-01-01'},
     ])
def test_invalid_attribute_name(xml, attribs):
    xml.calibrations(xml.measurand(xml.report(**attribs)))
    xml.raises(r"attribute 'foo' is not allowed")


@pytest.mark.parametrize('value', bad_dates)
def test_invalid_attribute_value(xml, value):
    xml.calibrations(xml.measurand(xml.report(date=value)))
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
def test_invalid_id_value(xml, value):
    xml.calibrations(xml.measurand(xml.report(id=value)))
    xml.raises('not accepted by the pattern')


@pytest.mark.parametrize(
    'value',
    ['   a   b   c ',
     'Radiometry/2023/123',
     'PTB 44183/12',
     '#987654-08',
     ])
def test_valid_id_value(xml, value):
    xml.calibrations(xml.measurand(xml.report(id=value)))
    assert xml.is_valid()


@pytest.mark.parametrize('value', bad_dates)
def test_invalid_start_value(xml, value):
    xml.calibrations(xml.measurand(xml.component(xml.report(start=value))))
    xml.raises(f"startDate': '{value}' is not a valid value")


@pytest.mark.parametrize('value', bad_dates)
def test_invalid_stop_value(xml, value):
    xml.calibrations(xml.measurand(xml.component(xml.report(stop=value))))
    xml.raises(f"stopDate': '{value}' is not a valid value")


def test_invalid_choice(xml):
    xml.calibrations(xml.measurand(xml.report(choice='<invalid/>')))
    xml.raises(r'Expected is one of .*equation, .*file, .*gtcArchive, .*table')
