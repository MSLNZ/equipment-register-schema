import pytest


@pytest.mark.parametrize(
    'text',
    ['MSLE.A.000',
     'MSLE.L.001',
     'MSLE.O.SP1234',
     'MSLE.Z.DRS',
     ])
def test_valid_pattern(xml, text):
    xml.id(text)
    assert xml.is_valid()


@pytest.mark.parametrize(
    'text',
    ['',  # empty
     ' ',  # no text
     '\n',  # no text
     'msl',  # does not start with MSLE nor contain .A.###
     'MSLE',  # does not contains .A.###
     'ABCD.E.F',  # does not start with MSLE
     'MSL-.A.0',  # hyphen instead of E
     'msle.a.0',  # lower case
     'MSLE-L.001',  # hyphen instead of dot
     'MSLE.L-001',  # hyphen instead of dot
     'MSLE.A.-1',  # contains hyphen
     'MSLE.A.1_',  # contains underscore
     'MSLE.A.b1',  # b is lower case
     'MSLE.A.0 ',  # ends with whitespace
     'MSLE. .0',  # contains whitespace
     ' MSLE.A.0',  # starts with whitespace
     'MSLE.A.\t000',  # contains tab
     'MSLE.A.000\t',  # contains tab
     '\tMSLE.A.000',  # contains tab
     ])
def test_invalid_pattern(xml, text):
    xml.id(text)
    xml.raises('not accepted by the pattern')


@pytest.mark.parametrize('occurances', [0, 2, 3, 10])
def test_one_occurance(xml, occurances):
    xml.id(occurances)
    xml.raises('manufacturer')  # <manufacturer> must be after <id>


def test_no_attributes(xml):
    xml.id('MSLE.A.000', foo='bar')
    xml.raises("attribute 'foo' is not allowed")
