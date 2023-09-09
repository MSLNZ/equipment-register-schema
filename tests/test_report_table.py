import pytest


def test_default(xml):
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=xml.table()))))
    assert xml.is_valid()


def test_missing_children(xml):
    xml.calibrations(xml.measurand(xml.component(xml.report(choice='<table/>'))))
    xml.raises('Missing child element')


def test_invalid_header_name(xml):
    xml.calibrations(xml.measurand(xml.component(xml.report(choice='<table><invalid/></table>'))))
    xml.raises(r'Expected is .*header')


@pytest.mark.parametrize(
    'header',
    ['',
     '    ',
     '\t',
     '\r',
     '\n',
     ',a',
     'a,',
     '   ,a',
     ' a,   ',
     ' a,b',  # cannot start with whitespace
     '\ta,b',  # cannot start with whitespace
     '\na,b',  # cannot start with whitespace
     'a,,b',
     ])
def test_invalid_header(xml, header):
    # not validating that header, datatype and data contain the same number of columns
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
     ])
def test_valid_header(xml, header):
    # not validating that header, datatype and data contain the same number of columns
    choice = xml.table(header=header)
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    assert xml.is_valid()


@pytest.mark.parametrize(
    'datatype',
    ['',
     '  ',
     ',int',
     'int,',
     ' ,int',
     ' int, ',
     'int,,float',
     'integer',
     'any,thing',
     'flo at',
     'int,float,bool,',
     ])
def test_invalid_datatype(xml, datatype):
    # not validating that header, datatype and data contain the same number of columns
    choice = xml.table(datatype=datatype)
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r'not accepted by the pattern')


@pytest.mark.parametrize(
    'datatype',
    ['int',
     '\nfloat',
     'bool\n',
     '   str    ',
     'date',
     'int, int, int',
     '    float,float,float,float,float,float,float,float,float,float',
     '\ndate,float,\n\n\nbool,                 str,int',
     ' bool , int , float , date , str ',
     ])
def test_valid_datatype(xml, datatype):
    # not validating that header, datatype and data contain the same number of columns
    choice = xml.table(datatype=datatype)
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    assert xml.is_valid()


@pytest.mark.parametrize(
    'data',
    ['',
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
    # not validating that header, datatype and data contain the same number of columns
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
    # not validating that header, datatype and data contain the same number of columns
    choice = xml.table(data=data)
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    assert xml.is_valid()
