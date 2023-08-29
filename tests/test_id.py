import pytest


@pytest.mark.parametrize(
    'text',
    ['MSLE.E.000',
     'MSLE.F.A01',
     'MSLE.H.1',
     'MSLE.L.X',
     'MSLE.M.AB001X',
     'MSLE.O.SP012',
     'MSLE.P.IDENTITY',
     'MSLE.T.00000000',
     ])
def test_valid_pattern(xml, text):
    xml.id(text)
    assert xml.is_valid()


@pytest.mark.parametrize(
    'text',
    ['',  # empty
     ' ',  # no text
     '\n',  # no text
     '\t',  # no text
     '\r',  # no text
     '   \t \r  \n',  # no text
     'msl',  # does not start with MSLE nor contain .A.###
     'MSLE',  # does not contains .A.###
     'ABCD.L.F',  # does not start with MSLE
     'MSL-.L.0',  # hyphen instead of E
     'msle.e.0',  # lower case
     'MSLE-L.001',  # hyphen instead of dot
     'MSLE.L-001',  # hyphen instead of dot
     'MSLE.L.-1',  # contains hyphen
     'MSLE.L.1_',  # contains underscore
     'MSLE.L.b1',  # b is lower case
     'MSLE.L.0 ',  # ends with whitespace
     'MSLE. L.0',  # contains whitespace
     ' MSLE.L.0',  # starts with whitespace
     'MSLE.L.\t000',  # contains tab
     'MSLE.L.000\n',  # contains new line
     'MSLE.L.000\r',  # contains carriage return
     ])
def test_invalid_pattern(xml, text):
    xml.id(text)
    xml.raises('not accepted by the pattern')


@pytest.mark.parametrize('occurances', [0, 2, 3, 10])
def test_one_occurance(xml, occurances):
    xml.id(occurances)
    xml.raises('manufacturer')  # <manufacturer> must be after <id>


def test_no_attributes(xml):
    xml.id('MSLE.L.000', foo='bar')
    xml.raises("attribute 'foo' is not allowed")
