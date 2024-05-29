import pytest


def test_missing_directory(xml):
    xml.calibrations(xml.measurand(xml.component(xml.report(choice='<file/>'))))
    xml.raises('Missing child element')


def test_invalid_subelement_name(xml):
    xml.calibrations(xml.measurand(xml.component(xml.report(choice='<file><invalid/></file>'))))
    xml.raises(r'Expected is .*directory')


def test_missing_filename(xml):
    choice = '<file><directory/></file>'
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r'Expected is .*filename')


def test_missing_sha256(xml):
    choice = '<file><directory/><filename>data.xlsx</filename></file>'
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r'Expected is .*sha256')


def test_extra_subelement(xml):
    choice = (f'<file>'
              f'  <directory>here</directory>'
              f'  <filename>data.dat</filename>'
              f'  <sha256>{xml.SHA256}</sha256>'
              f'  <sub/>'
              f'</file>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r'not expected')


def test_invalid_filename_name(xml):
    choice = '<file><directory/><directory/></file>'
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r'Expected is .*filename')


@pytest.mark.parametrize(
    'value',
    ['',
     '  ',
     'folder',
     'C:\\my\\calibration\\data',
     r'C:\my\calibration\data',
     'C:/my/calibration/data',
     'C:/my/cal ibr    ation/data/'
     'my/cal/data',
     ])
def test_directory_value(xml, value):
    # not testing that the directory exists, this should be validated by each team
    choice = (f'<file>'
              f'  <directory>{value}</directory>'
              f'  <filename>data.dat</filename>'
              f'  <sha256>{xml.SHA256}</sha256>'
              f'</file>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    assert xml.is_valid()


@pytest.mark.parametrize(
    'value',
    ['',
     '  ',
     '\t',
     '\n',
     '\r',
     '\n\r',
     '\n\n\n\n',
     '\t\t\t\t\t',
     ' \t\n',
     '\ndata.dat',
     'data.dat\n',
     '\rdata.dat',
     'data.dat\r',
     'data\n.dat',
     'd\ra\nta.dat',
     ])
def test_invalid_filename_value(xml, value):
    choice = f'<file><directory/><filename>{value}</filename></file>'
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises('not accepted by the pattern')


@pytest.mark.parametrize(
    'value',
    ['a',
     'data.dat',
     '/folder/data.dat',
     ' m y d    a t a .dat ',
     ])
def test_valid_filename_value(xml, value):
    # not testing that the file exists, this should be validated by each team
    choice = (f'<file>'
              f'  <directory/>'
              f'  <filename>{value}</filename>'
              f'  <sha256>{xml.SHA256}</sha256>'
              f'</file>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    assert xml.is_valid()


def test_filename_attributes(xml):
    choice = (f'<file>'
              f'  <directory/>'
              f'  <filename sheet="Sheet1" cell="A1:C20">data.xlsx</filename>'
              f'  <sha256>{xml.SHA256}</sha256>'
              f'</file>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    assert xml.is_valid()


@pytest.mark.parametrize(
    'checksum',
    ['c1062a18dad323b6da36a33f52f35cd8cb293413f5eeba41dee51ec1d904bbf5',  # lower case
     'C1062A18DAD323B6DA36A33F52F35CD8CB293413F5EEBA41DEE51EC1D904BBF5',  # upper case
     'c1062a18DAd323b6dA36A33f52F35cd8cB293413f5EEBa41dEE51ec1d904bbF5',  # mixed case
     ])
def test_sha256_valid(xml, checksum):
    choice = (f'<file>'
              f'  <directory/>'
              f'  <filename>data.xlsx</filename>'
              f'  <sha256>{checksum}</sha256>'
              f'</file>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    assert xml.is_valid()


@pytest.mark.parametrize(
    'checksum',
    ['', ' ', '\t', '\n', '\r', '\r\n',  # empty
     '8392e473a047543773138653b98037956fa2086e4a54fc882d913f10cc21772',    # too short
     '8392e473a047543773138653b98037956ga2086e4a54fc882d913f10cc217728',   # contains g
     '8392e473a047543773138653b98037956fa2086e4a54fc882d913f10cc217728a',  # too long
     ' c1062a18dad323b6da36a33f52f35cd8cb293413f5eeba41dee51ec1d904bbf5',  # leading space
     'c1062a18dad323b6da36a33f52f35cd8cb293413f5eeba41dee51ec1d904bbf5 ',  # trailing space
     ])
def test_sha256_invalid(xml, checksum):
    choice = (f'<file>'
              f'  <directory/>'
              f'  <filename>data.xlsx</filename>'
              f'  <sha256>{checksum}</sha256>'
              f'</file>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    assert not xml.is_valid()
