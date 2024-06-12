import pytest


def test_default(xml):
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=xml.table()))))
    assert xml.is_valid()


def test_missing_children(xml):
    xml.calibrations(xml.measurand(xml.component(xml.report(choice='<table/>'))))
    xml.raises('Missing child element')


def test_invalid_type_element_name(xml):
    t = '<table><invalid/></table>'
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=t))))
    xml.raises(r'Expected is .*type')


def test_invalid_header_element_name(xml):
    t = ('<table>'
         '  <type>int</type>'
         '  <invalid/>'
         '</table>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=t))))
    xml.raises(r'Expected is .*header')


def test_invalid_data_element_name(xml):
    t = ('<table>'
         '  <type>int</type>'
         '  <header>a</header>'
         '  <invalid/>'
         '</table>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=t))))
    xml.raises(r'Expected is .*data')


def test_invalid_extra_element_name(xml):
    t = ('<table>'
         '  <type>int</type>'
         '  <header>a</header>'
         '  <data>1</data>'
         '  <header>a</header>'
         '</table>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=t))))
    xml.raises(r'element is not expected')


@pytest.mark.parametrize(
    'header',
    ['',
     ',',
     ',a',
     ',,a',
     'a,',
     'a,,',
     'a,,b',
     'a,b,c,,',
     'a,b,c,,d',
     ])
def test_invalid_header(xml, header):
    # not validating that header, data type and data contain the same number of columns
    choice = xml.table(header=header)
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r'not accepted by the pattern')


@pytest.mark.parametrize(
    'header',
    ['a',
     '.',
     'a, b',
     'a ,b  ',
     'a,b,c,d',
     'a,\nb,\n\n\n\n\n          c,\nd\n',
     'a,\nb,\nc,\nd\n',
     'a , b , c , d ',
     'abc,def, ghi,jkl,    m n o p , qr,s,t,u,v, dut [mV] ',
     'a b, c d, e f, g h',
     'a bc, de f g, h i, jklmn (op), qr-stuv wxyz',
     '\n    wavelength (nm),\n    dark,\n    udark,\n    dut,\n    udut\n    ',
     ' a,b',
     '\ta,b',
     '\na,b',
     ' ,a',
     'a, ',
     ' ,a ',
     ' a, ',
     'a, ,b',  # the space is the name of the middle column
     'a, \n,b',  # the space\n is the name of the middle column
     'Wavelength [nm], Irradiance [W/m^2], Irradiance Std. Uncertainty [W/m^2]',
     ])
def test_valid_header(xml, header):
    # not validating that header, data type and data contain the same number of columns
    choice = xml.table(header=header)
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    assert xml.is_valid()


@pytest.mark.parametrize(
    'datatype',
    ['',
     ',',
     '  ',
     ',int',
     'int,',
     ' ,int',
     ' int, ',
     'int,,double',
     'int, ,double',
     'integer',
     'any,thing',
     'double,double,float',
     'doub le',
     'int,double,bool,',
     ])
def test_invalid_datatype(xml, datatype):
    # not validating that header, data type and data contain the same number of columns
    choice = xml.table(datatype=datatype)
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r'not accepted by the pattern')


@pytest.mark.parametrize(
    'datatype',
    ['int',
     '\ndouble',
     'bool\n',
     '   string    ',
     'int, int, int',
     '    double,double,double,double,double,double,double,double,double,double',
     '\ndouble,\n\n\nbool,                 string,int',
     ' bool , int , double , string ',
     ])
def test_valid_datatype(xml, datatype):
    # not validating that header, data type and data contain the same number of columns
    choice = xml.table(datatype=datatype)
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    assert xml.is_valid()


@pytest.mark.parametrize(
    'data',
    ['',
     ',',
     ',1',
     '1,',
     '1,,2',
     '1,2,3,4,',
     '\n1,2,3,4,\n',
     '1,2,3,\n4,5,6',
     '1,2,3\n4,5,6,',
     '1,2,3\n4,5,6\n,',
     ])
def test_invalid_data(xml, data):
    # not validating that header, data type and data contain the same number of columns
    choice = xml.table(data=data)
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r'not accepted by the pattern')


@pytest.mark.parametrize(
    'data',
    ['1',
     '1,2,3.0',
     '  1\n2\n3\n4\n5\n   ',
     '\n1,2,3.0\n1,2,3.0\n1,2,3.0\n',
     '     \n        1,     2,  3.0  \n    1  ,  2 , 3.0       \n1 ,2 ,         3.0\n         ',
     '12.3e-8,4.3e-8,50,false,text\n12.3e-8,4.3e-8,50,false,text\n12.3e-8,4.3e-8,50,false,text',
     ])
def test_valid_data(xml, data):
    # not validating that header, data type and data contain the same number of columns
    choice = xml.table(data=data)
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    assert xml.is_valid()
