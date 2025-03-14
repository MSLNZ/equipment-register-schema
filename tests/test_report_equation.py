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


def test_expect_unit_element(xml):
    choice = ('<equation>'
              '  <value variables="x">2*x</value>'
              '  <uncertainty variables="">1.0</uncertainty>'
              '  <invalid>3*x+1</invalid>'
              '</equation>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r'Expected is .*unit')


def test_expect_ranges_element(xml):
    choice = ('<equation>'
              '  <value variables="x">2*x</value>'
              '  <uncertainty variables="">1.0</uncertainty>'
              '  <unit>m</unit>'
              '  <invalid>3*x+1</invalid>'
              '</equation>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r'Expected is .*ranges')


def test_expect_degree_freedom_element(xml):
    choice = ('<equation>'
              '  <value variables="x">2*x</value>'
              '  <uncertainty variables="">1.0</uncertainty>'
              '  <unit>m</unit>'
              '  <ranges/>'
              '  <invalid>3*x+1</invalid>'
              '</equation>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r'Expected is .*degreeFreedom')


def test_extra_element(xml):
    choice = ('<equation>'
              '  <value variables="x">2*x</value>'
              '  <uncertainty variables="">1.0</uncertainty>'
              '  <unit>m</unit>'
              '  <ranges/>'
              '  <degreeFreedom>1</degreeFreedom>'
              '  <unknown/>'
              '</equation>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r"unknown': This element is not expected")


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
              f'  <unit>m</unit>'
              f'  <ranges/>'
              f'  <degreeFreedom>1</degreeFreedom>'
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
              f'  <unit>m</unit>'
              f'  <ranges/>'
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
              f'  <unit>m</unit>'
              f'  <ranges/>'
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
              f'  <unit>m</unit>'
              f'  <ranges/>'
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
              f'  <unit>m</unit>'
              f'  <ranges/>'
              f'</equation>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r'not accepted by the pattern')


@pytest.mark.parametrize(
    'uncertainty',
    ['2*x',
     '2*x ',
     ' 2*x',
     'x/123',
     '0.45 / 2.1',
     '     2 * x - 4.97124*sin(x/7.9187) + log(7.1*x**-0.3)',
     '\t2*x',
     '!)(*!^!%%',
     'anything with no line-feed nor carriage return character',
     ])
def test_valid_uncertainty_content(xml, uncertainty):
    choice = (f'<equation>'
              f'  <value variables="x">2*x</value>'
              f'  <uncertainty variables="">{uncertainty}</uncertainty>'
              f'  <unit>m</unit>'
              f'  <ranges/>'
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
              f'  <value variables="x">2*x</value>'
              f'  <uncertainty variables="{variables}">0.1</uncertainty>'
              f'  <unit>m</unit>'
              f'  <ranges/>'
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
              f'  <value variables="x">2*x</value>'
              f'  <uncertainty variables="{variables}">0.1</uncertainty>'
              f'  <unit>m</unit>'
              f'  <ranges/>'
              f'</equation>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    assert xml.is_valid()


@pytest.mark.parametrize(
    'unit',
    ['m',
     '\tm ',
     '°C',
     '\u00B0C',
     '%rh',
     'W/m^2',
     'W*m^(-2)',
     'W * m^{-2}',
     'anything with no line-feed nor carriage return character',
     ])
def test_valid_unit_content(xml, unit):
    choice = (f'<equation>'
              f'  <value variables="x">2*x</value>'
              f'  <uncertainty variables="">0.1</uncertainty>'
              f'  <unit>{unit}</unit>'
              f'  <ranges/>'
              f'</equation>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    assert xml.is_valid()


@pytest.mark.parametrize(
    'unit',
    ['',
     '\t',
     '\r',
     '\n',
     '\r\nm',
     'm\n',
     'contains a \newline character',
     ])
def test_invalid_unit_content(xml, unit):
    choice = (f'<equation>'
              f'  <value variables="x">2*x</value>'
              f'  <uncertainty variables="">0.1</uncertainty>'
              f'  <unit>{unit}</unit>'
              f'  <ranges/>'
              f'</equation>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r"not accepted by the pattern")


def test_range_attribute_missing(xml):
    choice = ('<equation>'
              '  <value variables="x">2*x</value>'
              '  <uncertainty variables="">0.1</uncertainty>'
              '  <unit>m</unit>'
              '  <ranges>'
              '    <range>'
              '      <minimum>1</minimum>'
              '      <maximum>1</maximum>'
              '    </range>'
              '  </ranges>'
              '</equation>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r"attribute 'variable' is required but missing")


def test_range_minimum_expected(xml):
    choice = ('<equation>'
              '  <value variables="x">2*x</value>'
              '  <uncertainty variables="">0.1</uncertainty>'
              '  <unit>m</unit>'
              '  <ranges>'
              '    <range variable="x">'
              '      <maximum>1</maximum>'
              '    </range>'
              '  </ranges>'
              '</equation>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r"maximum': This element is not expected")


def test_range_maximum_expected(xml):
    choice = ('<equation>'
              '  <value variables="x">2*x</value>'
              '  <uncertainty variables="">0.1</uncertainty>'
              '  <unit>m</unit>'
              '  <ranges>'
              '    <range variable="x">'
              '      <minimum>1</minimum>'
              '    </range>'
              '  </ranges>'
              '</equation>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r'Expected is .*maximum')


def test_range_maximum_twice(xml):
    choice = ('<equation>'
              '  <value variables="x">2*x</value>'
              '  <uncertainty variables="">0.1</uncertainty>'
              '  <unit>m</unit>'
              '  <ranges>'
              '    <range variable="x">'
              '      <minimum>1</minimum>'
              '      <maximum>2</maximum>'
              '      <maximum>2</maximum>'
              '    </range>'
              '  </ranges>'
              '</equation>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r"maximum': This element is not expected")


def test_range_minimum_invalid(xml):
    choice = ('<equation>'
              '  <value variables="x">2*x</value>'
              '  <uncertainty variables="">0.1</uncertainty>'
              '  <unit>m</unit>'
              '  <ranges>'
              '    <range variable="x">'
              '      <minimum>1.1d0</minimum>'
              '      <maximum>1</maximum>'
              '    </range>'
              '  </ranges>'
              '</equation>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r"'1.1d0' is not a valid value")


def test_range_maximum_invalid(xml):
    choice = ('<equation>'
              '  <value variables="x">2*x</value>'
              '  <uncertainty variables="">0.1</uncertainty>'
              '  <unit>m</unit>'
              '  <ranges>'
              '    <range variable="x">'
              '      <minimum>1.0</minimum>'
              '      <maximum>2.2d0</maximum>'
              '    </range>'
              '  </ranges>'
              '</equation>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r"'2.2d0' is not a valid value")


@pytest.mark.parametrize(
    'value', [1, 1.0001, 3.1415926, 0.0, -4.21e-6, '1.2345e6', 'INF', '-INF'])
def test_range_minimum_maximum_valid(xml, value):
    choice = (f'<equation>'
              f'  <value variables="x">2*x</value>'
              f'  <uncertainty variables="">0.1</uncertainty>'
              f'  <unit>m</unit>'
              f'  <ranges>'
              f'    <range variable="x">'
              f'      <minimum>{value}</minimum>'
              f'      <maximum>{value}</maximum>'
              f'    </range>'
              f'  </ranges>'
              f'</equation>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    assert xml.is_valid()


@pytest.mark.parametrize(
    'df',
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
def test_invalid_degree_freedom_content(xml, df):
    choice = (f'<equation>'
              f'  <value variables="x">2*x</value>'
              f'  <uncertainty variables="x">0.1/x</uncertainty>'
              f'  <unit>m</unit>'
              f'  <ranges/>'
              f'  <degreeFreedom>{df}</degreeFreedom>'
              f'</equation>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r'not a valid value')


@pytest.mark.parametrize('df', [-1, 0, 0.5, 0.9999, '-INF'])
def test_invalid_degree_freedom_min_inclusive(xml, df):
    choice = (f'<equation>'
              f'  <value variables="x">2*x</value>'
              f'  <uncertainty variables="">0.1</uncertainty>'
              f'  <unit>m</unit>'
              f'  <ranges/>'
              f'  <degreeFreedom>{df}</degreeFreedom>'
              f'</equation>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises("facet 'minInclusive'")


def test_invalid_degree_freedom_nan(xml):
    choice = (f'<equation>'
              f'  <value variables="x">2*x</value>'
              f'  <uncertainty variables="">0.1</uncertainty>'
              f'  <unit>m</unit>'
              f'  <ranges/>'
              f'  <degreeFreedom>NaN</degreeFreedom>'
              f'</equation>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises("facet 'maxInclusive'")


@pytest.mark.parametrize('df', [1, 1.0001, 3.1415926, '1.2345e6', 'INF'])
def test_valid_degree_freedom(xml, df):
    choice = (f'<equation>'
              f'  <value variables="x">2*x</value>'
              f'  <uncertainty variables="">0.1</uncertainty>'
              f'  <unit>m</unit>'
              f'  <ranges/>'
              f'  <degreeFreedom>{df}</degreeFreedom>'
              f'</equation>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    assert xml.is_valid()


@pytest.mark.parametrize('c', ['', ' ', '\t\t\t', 'BW:2nm', 'Can be any string!'])
def test_attribute_comment(xml, c):
    choice = (f'<equation comment="{c}">'
              f'  <value variables="x">2*x</value>'
              f'  <uncertainty variables="">0.1</uncertainty>'
              f'  <unit>m</unit>'
              f'  <ranges/>'
              f'</equation>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    assert xml.is_valid()


def test_attribute_unexpected(xml):
    choice = ('<equation apple="red">'
              '  <value variables="x">2*x</value>'
              '  <uncertainty variables="">0.1</uncertainty>'
              '  <unit>m</unit>'
              '  <ranges/>'
              '</equation>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r"attribute 'apple' is not allowed")
