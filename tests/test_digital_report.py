import pytest


def test_invalid_attribute_name(xml):
    xml.calibrations(xml.measurand(xml.component(xml.digital_report(fmt='MSL PDF/A-3'))))
    xml.raises(r"digitalReport', attribute 'fmt'")


def test_multiple_attributes(xml):
    xml.calibrations(xml.measurand(xml.component(xml.digital_report(format='MSL PDF/A-3', foo='foo'))))
    xml.raises(r"digitalReport', attribute 'foo'")


@pytest.mark.parametrize('fmt', ['MSL PDF/A-3', 'PTB DCC'])
def test_valid_attribute_value(xml, fmt):
    xml.calibrations(xml.measurand(xml.component(xml.digital_report(format=fmt, id='any', enteredBy='abc'))))
    assert xml.is_valid()


@pytest.mark.parametrize('fmt', [' MSL PDF/A-3', 'MSL PDF/A-3 ', 'MSL-PDF/A-3'])
def test_invalid_attribute_value(xml, fmt):
    xml.calibrations(xml.measurand(xml.component(xml.digital_report(format=fmt))))
    xml.raises(r"digitalReport'.*not an element of the set")


def test_invalid_choice_element(xml):
    e = xml.element('invalid')
    xml.calibrations(xml.measurand(xml.component(e)))
    xml.raises(r'Expected is one of .*digitalReport, .*report')


def test_invalid_url_element(xml):
    e = xml.element('invalid')
    xml.calibrations(xml.measurand(xml.component(xml.digital_report(url=e))))
    xml.raises(r'Expected is .*url')


def test_invalid_sha256_element(xml):
    e = xml.element('invalid')
    xml.calibrations(xml.measurand(xml.component(xml.digital_report(sha256=e))))
    xml.raises(r'Expected is .*sha256')


def test_extra_url_element(xml):
    e = (f'<digitalReport format="MSL PDF/A-3" id="any" enteredBy="Last, First">'
         f'  <url>file.pdf</url>'
         f'  <sha256>{xml.SHA256}</sha256>'
         f'  <url>file2.pdf</url>'
         f'</digitalReport>')
    xml.calibrations(xml.measurand(xml.component(e)))
    xml.raises(r"url': This element is not expected")


def test_extra_sha256_element(xml):
    e = (f'<digitalReport format="MSL PDF/A-3" id="any" enteredBy="x">'
         f'  <url>file.pdf</url>'
         f'  <sha256>{xml.SHA256}</sha256>'
         f'  <sha256>{xml.SHA256}</sha256>'
         f'</digitalReport>')
    xml.calibrations(xml.measurand(xml.component(e)))
    xml.raises(r"sha256': This element is not expected")


def test_multiple(xml):
    reports = '\n          '.join(str(xml.digital_report()) for _ in range(5))
    xml.calibrations(xml.measurand(xml.component(reports)))
    assert xml.is_valid()


@pytest.mark.parametrize('sequence', ['rrdrdd', 'rdr', 'ddrrrrr', 'drdrdrdrdrdrdr'])
def test_choice_mixed(xml, sequence):
    reports = '\n          '.join(
        xml.digital_report()
        if s == 'd' else xml.report()
        for s in sequence
    )
    xml.calibrations(xml.measurand(xml.component(reports)))
    assert xml.is_valid()


def test_url_with_attrib(xml):
    url = xml.element('url', text='cal.pdf', foo='bar', hello='world', apple='bright red')
    xml.calibrations(xml.measurand(xml.component(xml.digital_report(url=url))))
    assert xml.is_valid()


def test_sha256_with_attrib(xml):
    sha256 = xml.element('sha256', foo='bar')
    xml.calibrations(xml.measurand(xml.component(xml.digital_report(sha256=sha256))))
    xml.raises(r"sha256', attribute 'foo'")


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
    xml.calibrations(xml.measurand(xml.component(xml.digital_report(number=value))))
    xml.raises('not accepted by the pattern')


@pytest.mark.parametrize('c', ['', ' ', '\t\t\t', 'BW:2nm', 'Can be any string!'])
def test_attribute_comment(xml, c):
    attribs = {'id': 'a', 'comment': c, 'format': xml.FORMAT, 'enteredBy': 'a'}
    xml.calibrations(xml.measurand(xml.component(xml.digital_report(**attribs))))
    assert xml.is_valid()


@pytest.mark.parametrize('name', ['', '    '])
def test_entered_by_empty_string(xml, name):
    xml.calibrations(xml.measurand(xml.component(xml.digital_report(format='MSL PDF/A-3', id='any', enteredBy=name))))
    xml.raises('not accepted by the pattern')


@pytest.mark.parametrize('name', ['me', '', '    '])
def test_checked_by(xml, name):
    dr = xml.digital_report(format='MSL PDF/A-3', id='any', enteredBy='x', checkedBy=name)
    xml.calibrations(xml.measurand(xml.component(dr)))
    assert xml.is_valid()


def test_checked_date_valid(xml):
    dr = xml.digital_report(format='MSL PDF/A-3', id='any', enteredBy='x', checkedDate="2025-08-06")
    xml.calibrations(xml.measurand(xml.component(dr)))
    assert xml.is_valid()


def test_checked_date_invalid(xml):
    dr = xml.digital_report(format='MSL PDF/A-3', id='any', enteredBy='x', checkedDate="06-2025-08")
    xml.calibrations(xml.measurand(xml.component(dr)))
    xml.raises('not a valid value')
