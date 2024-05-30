import pytest


def test_missing_children(xml):
    choice = '<equation/>'
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises('Missing child element')


def test_invalid_value_element_name(xml):
    choice = ('<equation>'
              '  <invalid/>'
              '</equation>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r'Expected is .*value')


def test_missing_value_variables_attribute(xml):
    choice = ('<equation>'
              '  <value>2*x</value>'
              '</equation>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r'attribute \'variables\'')


def test_wrong_value_attribute_name(xml):
    choice = ('<equation>'
              '  <value banana="x">2*x</value>'
              '</equation>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r'attribute \'banana\'')


def test_extra_value_attribute(xml):
    choice = ('<equation>'
              '  <value variables="x" save="1">2*x</value>'
              '</equation>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r'attribute \'save\'')


def test_missing_uncertainty_element(xml):
    choice = ('<equation>'
              '  <value variables="x">2*x</value>'
              '</equation>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r'Expected is .*uncertainty')


def test_missing_uncertainty_variables_attribute(xml):
    choice = ('<equation>'
              '  <value variables="x">2*x</value>'
              '  <uncertainty>2</uncertainty>'
              '</equation>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r'attribute \'variables\'')


def test_wrong_uncertainty_attribute_name(xml):
    choice = ('<equation>'
              '  <value variables="x">2*x</value>'
              '  <uncertainty apple="x">2*x</uncertainty>'
              '</equation>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r'attribute \'apple\'')


def test_extra_uncertainty_attribute(xml):
    choice = ('<equation>'
              '  <value variables="x">2*x</value>'
              '  <uncertainty variables="x" save="1">2*x</uncertainty>'
              '</equation>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r'attribute \'save\'')


def test_missing_coverage_factor_element(xml):
    choice = ('<equation>'
              '  <value variables="x">2*x</value>'
              '  <uncertainty variables="">1.0</uncertainty>'
              '  <invalid>3*x+1</invalid>'
              '</equation>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r'Expected is .*coverageFactor')


def test_extra_element(xml):
    choice = ('<equation>'
              '  <value variables="x">2*x</value>'
              '  <uncertainty variables="">1.0</uncertainty>'
              '  <coverageFactor>1</coverageFactor>'
              '  <unknown/>'
              '</equation>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r'element is not expected')


@pytest.mark.parametrize(
    'value',
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
def test_invalid_value_content(xml, value):
    choice = (f'<equation>'
              f'  <value variables="x">{value}</value>'
              f'  <uncertainty variables="">0.1</uncertainty>'
              f'  <coverageFactor>1</coverageFactor>'
              f'</equation>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r'not accepted by the pattern')


@pytest.mark.parametrize(
    'value',
    ['2*x',
     '2*x ',
     ' 2*x',
     'x/123',
     '     2 * x - 4.97124*sin(x/7.9187) + log(7.1*x**-0.3)',
     '\t2*x',
     '!)(*!^!%%',
     'anything with no line-feed nor carriage return character',
     ])
def test_valid_value_content(xml, value):
    choice = (f'<equation>'
              f'  <value variables="x">{value}</value>'
              f'  <uncertainty variables="">1</uncertainty>'
              f'  <coverageFactor>1</coverageFactor>'
              f'</equation>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    assert xml.is_valid()


@pytest.mark.parametrize(
    'variables',
    [',',
     '_',
     '1',
     '1x',
     '_x',
     '*x',
     'x,',
     'x,y',
     'x , y',
     'x1 , y1',
     ])
def test_invalid_value_variables(xml, variables):
    choice = (f'<equation>'
              f'  <value variables="{variables}">2*x</value>'
              f'  <uncertainty variables="">0.1</uncertainty>'
              f'  <coverageFactor>1</coverageFactor>'
              f'</equation>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r'not accepted by the pattern')


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
     'x',
     'X',
     'x1',
     'x_1 x_2 x_2345',
     'x Y     z',
     ' jsjlj28 x89____yhj98js        k98HYS_j89j3JSA_89j9   '
     ])
def test_valid_value_variables(xml, variables):
    choice = (f'<equation>'
              f'  <value variables="{variables}">2*x</value>'
              f'  <uncertainty variables="">0.1</uncertainty>'
              f'  <coverageFactor>1</coverageFactor>'
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
     '2*x\n',
     '2*x\r\n',
     '\n2*x',
     ])
def test_invalid_uncertainty_content(xml, uncertainty):
    choice = (f'<equation>'
              f'  <value variables="x">2*x</value>'
              f'  <uncertainty variables="">{uncertainty}</uncertainty>'
              f'  <coverageFactor>1</coverageFactor>'
              f'</equation>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r'not accepted by the pattern')


@pytest.mark.parametrize(
    'uncertainty',
    ['2*x',
     '2*x ',
     ' 2*x',
     'x/123',
     '     2 * x - 4.97124*sin(x/7.9187) + log(7.1*x**-0.3)',
     '\t2*x',
     '!)(*!^!%%',
     'anything with no line-feed nor carriage return character',
     ])
def test_valid_uncertainty_content(xml, uncertainty):
    choice = (f'<equation>'
              f'  <value variables="x">2*x</value>'
              f'  <uncertainty variables="">{uncertainty}</uncertainty>'
              f'  <coverageFactor>1</coverageFactor>'
              f'</equation>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    assert xml.is_valid()


@pytest.mark.parametrize(
    'variables',
    [',',
     '_',
     '1',
     '1x',
     '_x',
     '*x',
     'x,',
     'x,y',
     'x , y',
     'x1 , y1',
     ])
def test_invalid_uncertainty_variables(xml, variables):
    choice = (f'<equation>'
              f'  <value variables="">2*x</value>'
              f'  <uncertainty variables="{variables}">0.1</uncertainty>'
              f'  <coverageFactor>1</coverageFactor>'
              f'</equation>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r'not accepted by the pattern')


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
     'x',
     'X',
     'x1',
     'x_1 x_2 x_2345',
     'x Y     z',
     ' jsjlj28 x89____yhj98js        k98HYS_j89j3JSA_89j9   '
     ])
def test_valid_uncertainty_variables(xml, variables):
    choice = (f'<equation>'
              f'  <value variables="">2*x</value>'
              f'  <uncertainty variables="{variables}">0.1</uncertainty>'
              f'  <coverageFactor>1</coverageFactor>'
              f'</equation>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    assert xml.is_valid()


@pytest.mark.parametrize(
    'cf',
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
def test_invalid_coverage_factor_content(xml, cf):
    choice = (f'<equation>'
              f'  <value variables="x">2*x</value>'
              f'  <uncertainty variables="x">0.1/x</uncertainty>'
              f'  <coverageFactor>{cf}</coverageFactor>'
              f'</equation>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r'not a valid value')


@pytest.mark.parametrize(
    ('cf', 'facet'),
    [(0.99, 'minInclusive'),
     (12.71, 'maxInclusive'),
    ])
def test_invalid_coverage_factor_range(xml, cf, facet):
    choice = (f'<equation>'
              f'  <value variables="x">2*x</value>'
              f'  <uncertainty variables="">0.1</uncertainty>'
              f'  <coverageFactor>{cf}</coverageFactor>'
              f'</equation>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(f'facet {facet!r}')


@pytest.mark.parametrize('cf', [1, 1.0001, 3.1415926, 12.7])
def test_valid_coverage_factor(xml, cf):
    choice = (f'<equation>'
              f'  <value variables="x">2*x</value>'
              f'  <uncertainty variables="">0.1</uncertainty>'
              f'  <coverageFactor>{cf}</coverageFactor>'
              f'</equation>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    assert xml.is_valid()
