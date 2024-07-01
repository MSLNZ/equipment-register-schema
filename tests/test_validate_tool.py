import sys
from io import StringIO
from pathlib import Path

import pytest
from lxml.builder import E

from tools import validate

parent = Path(__file__).parent
file_paths = [
    parent / 'do_not_modify_this_file.txt',
    f'{parent}/do_not_modify_this_file.txt',
    f'file:{parent}/do_not_modify_this_file.txt',  # rfc8089#appendix-E.2
    f'file://{parent}/do_not_modify_this_file.txt',
    f'file:///{parent}/do_not_modify_this_file.txt',
    'tests/do_not_modify_this_file.txt',
    'file:tests/do_not_modify_this_file.txt',
]

if sys.platform == 'win32':
    file_paths.extend([
        f'{parent}\\do_not_modify_this_file.txt',
        rf'{parent}\do_not_modify_this_file.txt',
        f'file:{parent}\\do_not_modify_this_file.txt',  # rfc8089#appendix-E.2
        rf'file:{parent}\do_not_modify_this_file.txt',  # rfc8089#appendix-E.2
        f'file://{parent}\\do_not_modify_this_file.txt',
        rf'file://{parent}\do_not_modify_this_file.txt',
        f'file:///{parent}\\do_not_modify_this_file.txt',  # rfc8089#appendix-E.2
        rf'file:///{parent}\do_not_modify_this_file.txt',
        'tests\\do_not_modify_this_file.txt',
        r'tests\do_not_modify_this_file.txt',
        'file:///tests/do_not_modify_this_file.txt',
        'file:///tests\\do_not_modify_this_file.txt',
        r'file:///tests\do_not_modify_this_file.txt',
        'file:tests\\do_not_modify_this_file.txt',
        r'file:tests\do_not_modify_this_file.txt',
    ])


def test_file_path_invalid(xml):
    file = (
        f'<file>'
        f'  <url>file.txt</url>'
        f'  <sha256>{xml.SHA256}</sha256>'
        f'</file>'
    )
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=file))))
    with pytest.raises(FileNotFoundError):
        validate.validate(StringIO(repr(xml)))


def test_file_root_specified(xml):
    file = (
        '<file>'
        '  <url>do_not_modify_this_file.txt</url>'
        '  <sha256>699521aa6d52651ef35ee84232f657490eb870543119810f2af8bc68496d693c</sha256>'
        '</file>'
    )
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=file))))
    validate.validate(StringIO(repr(xml)), root_dir='tests')


def test_file_unsupported_url_scheme(xml):
    file = (
        f'<file>'
        f'  <url>ftp://msl/data.pdf</url>'
        f'  <sha256>{xml.SHA256}</sha256>'
        f'</file>'
    )
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=file))))
    with pytest.raises(ValueError, match=r"url scheme 'ftp'"):
        validate.validate(StringIO(repr(xml)))


def test_file_invalid_checksum(xml):
    here = Path(__file__)
    file = (
        f'<file>'
        f'  <url>file://{here.parent}/{here.name}</url>'
        f'  <sha256>{xml.SHA256}</sha256>'
        f'</file>'
    )
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=file))))
    with pytest.raises(AssertionError, match=r'SHA-256 checksum'):
        validate.validate(StringIO(repr(xml)))


@pytest.mark.parametrize('url', file_paths)
def test_file_valid(xml, url):
    file = (
        f'<file>'
        f'  <url>{url}</url>'
        f'  <sha256>699521aa6d52651ef35ee84232f657490eb870543119810f2af8bc68496d693c</sha256>'
        f'</file>'
    )
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=file))))
    validate.validate(StringIO(repr(xml)))


def test_digital_report_path_invalid(xml):
    report = xml.digital_report(url='file.txt')
    xml.calibrations(xml.measurand(xml.component(report)))
    with pytest.raises(FileNotFoundError):
        validate.validate(StringIO(repr(xml)))


def test_digital_report_root_specified(xml):
    report = xml.digital_report(
        url='do_not_modify_this_file.txt',
        sha256='699521aa6d52651ef35ee84232f657490eb870543119810f2af8bc68496d693c',
    )
    xml.calibrations(xml.measurand(xml.component(report)))
    validate.validate(StringIO(repr(xml)), root_dir='tests')


def test_digital_report_unsupported_url_scheme(xml):
    report = xml.digital_report(url='ftp://msl/data.pdf')
    xml.calibrations(xml.measurand(xml.component(report)))
    with pytest.raises(ValueError, match=r"url scheme 'ftp'"):
        validate.validate(StringIO(repr(xml)))


def test_digital_report_invalid_checksum(xml):
    here = Path(__file__)
    report = xml.digital_report(
        url=f'file://{here.parent}/{here.name}',
        sha256=xml.SHA256,
    )
    xml.calibrations(xml.measurand(xml.component(report)))
    with pytest.raises(AssertionError, match=r'SHA-256 checksum'):
        validate.validate(StringIO(repr(xml)))


@pytest.mark.parametrize('url', file_paths)
def test_digital_report_valid(xml, url):
    report = xml.digital_report(
        url=url,
        sha256='699521aa6d52651ef35ee84232f657490eb870543119810f2af8bc68496d693c',
    )
    xml.calibrations(xml.measurand(xml.component(report)))
    validate.validate(StringIO(repr(xml)))


def test_serialized_ignored_format():
    validate._serialised(E.serialised(E.ignore('serialised text')), debug_name='whatever')


def test_serialized_gtc_archive_valid(xml):
    serialised = (
        '<serialised>'
        '  <gtcArchive version="1.5.0" xmlns="https://measurement.govt.nz/gtc/xml">'
        '    <leafNodes>'
        '      <leafNode uid="(1, 1)">'
        '        <u>1.0</u>'
        '        <df>INF</df>'
        '        <label />'
        '        <independent>true</independent>'
        '      </leafNode>'
        '    </leafNodes>'
        '    <taggedReals>'
        '      <elementaryReal tag="x" uid="(1, 1)">'
        '        <value>1.0</value>'        
        '      </elementaryReal>'
        '    </taggedReals>'
        '    <untaggedReals />'
        '    <taggedComplexes />'
        '    <intermediates />'
        '  </gtcArchive>'
        '</serialised>'
    )
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=serialised))))
    validate.validate(StringIO(repr(xml)))


def test_serialized_gtc_archive_invalid(xml):
    serialised = (
        '<serialised>'
        '  <gtcArchive version="1.5.0" xmlns="https://measurement.govt.nz/gtc/xml">'
        '    <leafNodes>'
        '      <leafNode uid="(1, 1)">'
        '        <u>1.0</u>'
        '        <df>INF</df>'
        '        <label />'
        '        <independent>true</independent>'
        '      </leafNode>'
        '    </leafNodes>'
        '    <taggedReals>'
        '      <elementaryReal tag="x" uid="(2, 1)">'  # does not match uid="(1, 1)"
        '        <value>1.0</value>'        
        '      </elementaryReal>'
        '    </taggedReals>'
        '    <untaggedReals />'
        '    <taggedComplexes />'
        '    <intermediates />'
        '  </gtcArchive>'
        '</serialised>'
    )
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=serialised))))
    with pytest.raises(AssertionError, match=r'Invalid serialised GTC Archive'):
        validate.validate(StringIO(repr(xml)))


def test_serialised_gtc_archive_json_valid(xml):
    serialised = (
        '<serialised>'
        '  <gtcArchiveJSON>{'
        '    "CLASS": "Archive",'
        '    "version": "https://measurement.govt.nz/gtc/json_1.5.0",'
        '    "leaf_nodes": {'
        '      "(1, 1)": {'
        '        "CLASS": "LeafNode",'
        '        "uid": "(1, 1)",'
        '        "label": null,'
        '        "u": 1.0,'
        '        "df": null,'
        '        "independent": true'
        '      }'
        '    },'
        '    "tagged_real": {'
        '      "x": {'
        '        "CLASS": "ElementaryReal",'
        '        "x": 1.0,'
        '        "uid": "(1, 1)"'
        '      }'
        '    },'
        '    "tagged_complex": {},'
        '    "untagged_real": {},'
        '    "intermediate_uids": {}'
        '  }</gtcArchiveJSON>'
        '</serialised>'
    )
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=serialised))))
    validate.validate(StringIO(repr(xml)))


def test_serialised_gtc_archive_json_invalid(xml):
    serialised = (
        '<serialised>'
        '  <gtcArchiveJSON>{'
        '    "CLASS": "Archive",'
        '    "version": "https://measurement.govt.nz/gtc/json_1.5.0",'
        '    "leaf_nodes": {'
        '      "(1, 1)": {'
        '        "CLASS": "LeafNode",'
        '        "uid": "(1, 1)",'
        '        "label": null,'
        '        "u": 1.0,'
        '        "df": null,'
        '        "independent": true'
        '      }'
        '    },'
        '    "tagged_real": {'
        '      "x": {'
        '        "CLASS": "ElementaryReal",'
        '        "x": 1.0,'
        '        "uid": "(2, 1)"'  # does not match uid="(1, 1)"
        '      }'
        '    },'
        '    "tagged_complex": {},'
        '    "untagged_real": {},'
        '    "intermediate_uids": {}'
        '  }</gtcArchiveJSON>'
        '</serialised>'
    )
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=serialised))))
    with pytest.raises(AssertionError, match=r'Invalid serialised GTC Archive'):
        validate.validate(StringIO(repr(xml)))


def test_table_data_valid(xml):
    table = (
        '<table>'
        '  <type>  bool,  int,double,string</type>'
        '  <unit>      ,   nm,   %rh,      </unit>'
        '  <header>col1, col2,  col3,  col4</header>'
        '  <data>\ntrue,  123,  5e-6, foobar\n\n\n'
        '             1,   -1,  -6e6, T °C\n</data>'
        '</table>'
    )
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=table))))
    validate.validate(StringIO(repr(xml)))


def test_table_type_unit_length_unequal(xml):
    table = (
        '<table>'
        '  <type>bool,int</type>'
        '  <unit>nm</unit>'
        '  <header>column</header>'
        '  <data>true,2</data>'
        '</table>'
    )
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=table))))
    with pytest.raises(AssertionError, match=r'"type" and "unit" have different lengths'):
        validate.validate(StringIO(repr(xml)))


def test_table_type_header_length_unequal(xml):
    table = (
        '<table>'
        '  <type>bool,int</type>'
        '  <unit>    , nm</unit>'
        '  <header>column</header>'
        '  <data>true,2</data>'
        '</table>'
    )
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=table))))
    with pytest.raises(AssertionError, match=r'"type" and "header" have different lengths'):
        validate.validate(StringIO(repr(xml)))


def test_table_type_data_length_unequal(xml):
    table = (
        '<table>'
        '  <type>  bool,int</type>'
        '  <unit>      , nm</unit>'
        '  <header>col1,col</header>'
        '  <data>  true,  2, 6.7</data>'
        '</table>'
    )
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=table))))
    with pytest.raises(AssertionError, match=r"row data is 'true,  2, 6.7'"):
        validate.validate(StringIO(repr(xml)))


@pytest.mark.parametrize('value', ['true', 'True', 'TRUE', '1', 'false', 'False', 'FALSE', '0'])
def test_table_bool_valid(xml, value):
    table = (
        f'<table>'
        f'  <type>bool,int</type>'
        f'  <unit>    , nm</unit>'
        f'  <header>col1,col2</header>'
        f'  <data>{value},2</data>'
        f'</table>'
    )
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=table))))
    validate.validate(StringIO(repr(xml)))


def test_table_bool_invalid(xml):
    table = (
        '<table>'
        '  <type>bool,int</type>'
        '  <unit>    , nm</unit>'
        '  <header>col1,col2</header>'
        '  <data>INVALID,2</data>'
        '</table>'
    )
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=table))))
    with pytest.raises(AssertionError, match=r'one of: true, True, TRUE, 1, false, False, FALSE, 0'):
        validate.validate(StringIO(repr(xml)))


@pytest.mark.parametrize('value', ['-2147483649', '2147483648'])
def test_table_int_invalid_range(xml, value):
    table = (
        f'<table>'
        f'  <type>bool,int</type>'
        f'  <unit>    , nm</unit>'
        f'  <header>col1,col2</header>'
        f'  <data>true,{value}</data>'
        f'</table>'
    )
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=table))))
    with pytest.raises(AssertionError, match=r'range \[-2147483648, 2147483647\]'):
        validate.validate(StringIO(repr(xml)))


@pytest.mark.parametrize('value', ['string', '1.2'])
def test_table_int_invalid_value(xml, value):
    table = (
        f'<table>'
        f'  <type>bool,int</type>'
        f'  <unit>    , nm</unit>'
        f'  <header>col1,col2</header>'
        f'  <data>true,{value}</data>'
        f'</table>'
    )
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=table))))
    with pytest.raises(AssertionError, match=r'invalid literal for int'):
        validate.validate(StringIO(repr(xml)))


@pytest.mark.parametrize('value', ['string', '1.2f0'])
def test_table_float_invalid_value(xml, value):
    table = (
        f'<table>'
        f'  <type>bool,double</type>'
        f'  <unit>    , nm</unit>'
        f'  <header>col1,col2</header>'
        f'  <data>true,{value}</data>'
        f'</table>'
    )
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=table))))
    with pytest.raises(AssertionError, match=r'string to float'):
        validate.validate(StringIO(repr(xml)))


def test_equation_valid(xml):
    equation = (
        '<equation>'
        '  <value variables="x y z">'
        '  0.1 * x \t    '
        '  + 2.3e-5 * pow(y, 2) '
        '  - sqrt(0.2*x) '
        '  + sin((0.1*x+1.1))'
        '  - asin(0.1)'
        '  + cos(0.1)'
        '  - acos(0.1)'
        '  + tan(0.4)'
        '  - atan(0.1)'
        '  + exp(0.2)'
        '  - log(2.1)'
        '  + log10(1.1)'
        '  + 2*pi/z'
        '  </value>'
        '  <uncertainty variables="">1.0</uncertainty>'
        '  <unit>m</unit>'
        '  <ranges>'
        '    <range variable="x">'
        '      <minimum>1</minimum>'
        '      <maximum>2</maximum>'
        '    </range>'
        '    <range variable="y">'
        '      <minimum>10</minimum>'
        '      <maximum>20</maximum>'
        '    </range>'
        '    <range variable="z">'
        '      <minimum>1e2</minimum>'
        '      <maximum>2e2</maximum>'
        '    </range>'
        '  </ranges>'
        '</equation>'
    )
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=equation))))
    validate.validate(StringIO(repr(xml)))


def test_equation_variables_passed(xml):
    equation = (
        '<equation>'
        '  <value variables="x">log(x)</value>'
        '  <uncertainty variables="">1.0</uncertainty>'
        '  <unit>m</unit>'
        '  <ranges>'
        '    <range variable="x">'
        '      <minimum>1</minimum>'
        '      <maximum>2</maximum>'
        '    </range>'
        '  </ranges>'
        '</equation>'
    )
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=equation))))

    # equation is valid syntax (so no error is raised)
    with pytest.warns(RuntimeWarning, match=r'invalid value encountered in log'):
        validate.validate(StringIO(repr(xml)), x=-1)


def test_equation_missing_bracket(xml):
    equation = (
        '<equation>'
        '  <value variables="x">1.2 + 0.2*pow(x,3) - ((6+2/x)*sin(1.0) </value>'
        '  <uncertainty variables="">1.0</uncertainty>'
        '  <unit>m</unit>'
        '  <ranges>'
        '    <range variable="x">'
        '      <minimum>1</minimum>'
        '      <maximum>2</maximum>'
        '    </range>'
        '  </ranges>'
        '</equation>'
    )
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=equation))))
    with pytest.raises(AssertionError, match=r'SyntaxError'):
        validate.validate(StringIO(repr(xml)))


def test_equation_unknown_function(xml):
    equation = (
        '<equation>'
        '  <value variables="x">1.2 + 0.2*arccos(0.1*x)</value>'
        '  <uncertainty variables="">1.0</uncertainty>'
        '  <unit>m</unit>'
        '  <ranges>'
        '    <range variable="x">'
        '      <minimum>1</minimum>'
        '      <maximum>2</maximum>'
        '    </range>'
        '  </ranges>'
        '</equation>'
    )
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=equation))))
    with pytest.raises(AssertionError, match=r'NameError'):
        validate.validate(StringIO(repr(xml)))


def test_equation_range_variables_unique(xml):
    equation = (
        '<equation>'
        '  <value variables="x">1.2 + 0.2*arccos(0.1*x)</value>'
        '  <uncertainty variables="">1.0</uncertainty>'
        '  <unit>m</unit>'
        '  <ranges>'
        '    <range variable="x">'
        '      <minimum>1</minimum>'
        '      <maximum>2</maximum>'
        '    </range>'
        '    <range variable="y">'
        '      <minimum>10</minimum>'
        '      <maximum>20</maximum>'
        '    </range>'
        '    <range variable="x">'
        '      <minimum>1e2</minimum>'
        '      <maximum>2e2</maximum>'
        '    </range>'
        '  </ranges>'
        '</equation>'
    )
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=equation))))
    with pytest.raises(AssertionError, match=r'variable names: x, x, y'):
        validate.validate(StringIO(repr(xml)))


def test_equation_range_variable_missing(xml):
    equation = (
        '<equation>'
        '  <value variables="x y">x+y</value>'
        '  <uncertainty variables="v">0.1*v</uncertainty>'
        '  <unit>m</unit>'
        '  <ranges>'
        '    <range variable="x">'
        '      <minimum>1</minimum>'
        '      <maximum>2</maximum>'
        '    </range>'
        '    <range variable="y">'
        '      <minimum>1</minimum>'
        '      <maximum>2</maximum>'
        '    </range>'
        '  </ranges>'
        '</equation>'
    )
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=equation))))
    match = r"equation variables: v, x, y\nrange variables   : x, y"
    with pytest.raises(AssertionError, match=match):
        validate.validate(StringIO(repr(xml)))


def test_equation_range_variable_extra(xml):
    equation = (
        '<equation>'
        '  <value variables="x">x+1</value>'
        '  <uncertainty variables="">0.1</uncertainty>'
        '  <unit>m</unit>'
        '  <ranges>'
        '    <range variable="x">'
        '      <minimum>1</minimum>'
        '      <maximum>2</maximum>'
        '    </range>'
        '    <range variable="y">'
        '      <minimum>1</minimum>'
        '      <maximum>2</maximum>'
        '    </range>'
        '  </ranges>'
        '</equation>'
    )
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=equation))))
    match = r"equation variables: x\nrange variables   : x, y"
    with pytest.raises(AssertionError, match=match):
        validate.validate(StringIO(repr(xml)))


def test_equation_range_variable_name_wrong(xml):
    equation = (
        '<equation>'
        '  <value variables="x y">x+y</value>'
        '  <uncertainty variables="value">0.1*value</uncertainty>'
        '  <unit>m</unit>'
        '  <ranges>'
        '    <range variable="x">'
        '      <minimum>1</minimum>'
        '      <maximum>2</maximum>'
        '    </range>'
        '    <range variable="y">'
        '      <minimum>1</minimum>'
        '      <maximum>2</maximum>'
        '    </range>'
        '    <range variable="z">'
        '      <minimum>1</minimum>'
        '      <maximum>2</maximum>'
        '    </range>'
        '  </ranges>'
        '</equation>'
    )
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=equation))))
    match = r"equation variables: value, x, y\nrange variables   : x, y, z"
    with pytest.raises(AssertionError, match=match):
        validate.validate(StringIO(repr(xml)))


def test_equation_no_variables(xml):
    equation = (
        '<equation>'
        '  <value variables="">1</value>'
        '  <uncertainty variables="">0.1</uncertainty>'
        '  <unit>m</unit>'
        '  <ranges/>'
        '</equation>'
    )
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=equation))))
    validate.validate(StringIO(repr(xml)))


def test_recursive():
    assert validate.recursive_validate('./examples') > 0


def test_duplicate_id():
    match = r"Duplicate equipment ID, 'MSLE.M.002',"
    with pytest.raises(AssertionError, match=match):
        validate.recursive_validate('./tests/registers')
