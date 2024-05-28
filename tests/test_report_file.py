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
              f'  <sha256>8392e473a047543773138653b98037956fa2086e4a54fc882d913f10cc217728</sha256>'
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
              f'  <sha256>8392e473a047543773138653b98037956fa2086e4a54fc882d913f10cc217728</sha256>'
              f'</file>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    assert xml.is_valid()


def test_filename_attributes(xml):
    choice = ('<file>'
              '  <directory/>'
              '  <filename sheet="Sheet1" cell="A1:C20">data.xlsx</filename>'
              '  <sha256>8392e473a047543773138653b98037956fa2086e4a54fc882d913f10cc217728</sha256>'
              '</file>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    assert xml.is_valid()


@pytest.mark.parametrize(
    'checksum',
    ['8392e473a047',  # too short
     'J392e473a047543773138653b98037956fa2086e4a54fc882d913f10cc217728',  # contains J
     ])
def test_sha256_invalid(xml, checksum):
    choice = (f'<file>'
              f'  <directory/>'
              f'  <filename>data.xlsx</filename>'
              f'  <sha256>{checksum}</sha256>'
              f'</file>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    assert not xml.is_valid()


def test_sha256_missing(xml):
    choice = '<file><directory/><filename>data.xlsx</filename></file>'
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r'Expected is .*sha256')
