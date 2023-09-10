import pytest


def test_missing_children(xml):
    choice = '<equation/>'
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises('Missing child element')


def test_invalid_parse_element_name(xml):
    choice = ('<equation>'
              '  <invalid/>'
              '</equation>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r'Expected is .*parse')


def test_missing_variables_element(xml):
    choice = ('<equation>'
              '  <parse>2*x</parse>'
              '</equation>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r'Expected is .*variables')


def test_missing_uncertainty_element(xml):
    choice = ('<equation>'
              '  <parse>2*x</parse>'
              '  <variables>x</variables>'
              '</equation>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r'Expected is .*uncertainty')


def test_parse_element_repeats(xml):
    choice = ('<equation>'
              '  <parse>2*x</parse>'
              '  <variables>x</variables>'
              '  <uncertainty>1.0</uncertainty>'
              '  <parse>3*x+1</parse>'
              '</equation>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r'element is not expected')


@pytest.mark.parametrize(
    'parse',
    ['',
     '     ',
     '\t',
     '\n',
     '\r',
     '\n\r',
     '\n\n\n\n',
     '\t\t\t\t\t',
     ' \t\n',
     '2*x\n',
     '2*x\r\n',
     '\n2*x',
     ])
def test_invalid_parse_content(xml, parse):
    choice = (f'<equation>'
              f'  <parse>{parse}</parse>'
              f'  <variables>x</variables>'
              f'  <uncertainty>0.1</uncertainty>'
              f'</equation>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r'not accepted by the pattern')


@pytest.mark.parametrize(
    'parse',
    ['2*x',
     '2*x ',
     ' 2*x',
     '     2 * x - 4.97124*sin(x/7.9187) + log(7.1*x**-0.3)',
     '\t2*x',
     '!)(*!^!%%',
     'anything with no line-feed nor carriage return character',
     ])
def test_valid_parse_content(xml, parse):
    choice = (f'<equation>'
              f'  <parse>{parse}</parse>'
              f'  <variables>x</variables>'
              f'  <uncertainty>0.1</uncertainty>'
              f'</equation>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    assert xml.is_valid()


@pytest.mark.parametrize(
    'variables',
    ['',
     '     ',
     '\t',
     '\n',
     '\r',
     '\n\r',
     '\n\n\n\n',
     '\t\t\t\t\t',
     ' \t\n',
     ',',
     '1x',
     '_x',
     'x_1',
     'x1, x2',
     'x ,y',
     'x,y,',
     'x,y,,z',
     ])
def test_invalid_variables_content(xml, variables):
    choice = (f'<equation>'
              f'  <parse>2*x</parse>'
              f'  <variables>{variables}</variables>'
              f'  <uncertainty>0.1</uncertainty>'
              f'</equation>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r'not accepted by the pattern')


@pytest.mark.parametrize(
    'variables',
    ['x',
     'X',
     'x1',
     'x,y,z',
     'jsjlj28,x89yhj98js,k98j89j32d89j9,d83u'
     ])
def test_valid_variables_content(xml, variables):
    choice = (f'<equation>'
              f'  <parse>2*x</parse>'
              f'  <variables>{variables}</variables>'
              f'  <uncertainty>0.1</uncertainty>'
              f'</equation>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    assert xml.is_valid()


@pytest.mark.parametrize(
    'uncertainty',
    ['',
     '     ',
     '\t',
     '\n',
     '\r',
     '\n\r',
     '\n\n\n\n',
     '\t\t\t\t\t',
     ' \t\n',
     '1d0',
     '1. 0982',
     '-1.0 e-4',
     ])
def test_invalid_uncertainty_content(xml, uncertainty):
    choice = (f'<equation>'
              f'  <parse>2*x</parse>'
              f'  <variables>x</variables>'
              f'  <uncertainty>{uncertainty}</uncertainty>'
              f'</equation>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r'not a valid value')


def test_negative_uncertainty_value(xml):
    choice = (f'<equation>'
              f'  <parse>2*x</parse>'
              f'  <variables>x</variables>'
              f'  <uncertainty>-1.0</uncertainty>'
              f'</equation>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r'less than the minimum value')


@pytest.mark.parametrize(
    'uncertainty',
    ['0',
     '0.0',
     '0e0',
     '0.9871652',
     '+1e0',
     '32.4e-1',
     '3.45678e-01',
     '3.4e+10',
     ])
def test_valid_uncertainty_content(xml, uncertainty):
    choice = (f'<equation>'
              f'  <parse>2*x</parse>'
              f'  <variables>x</variables>'
              f'  <uncertainty>{uncertainty}</uncertainty>'
              f'</equation>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    assert xml.is_valid()
