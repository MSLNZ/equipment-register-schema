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
    xml.raises("id', attribute 'foo'")


def test_unique(xml):
    xml1 = xml()
    xml1.id('MSLE.L.001')
    xml2 = xml()
    xml2.id('MSLE.L.002')
    xml3 = xml()
    xml3.id('MSLE.L.003')
    xml4 = xml()
    xml4.id('MSLE.L.004')

    lines = repr(xml1).splitlines()[1:-1]  # skip XML declaration and </register>
    lines.extend(repr(xml2).splitlines()[2:-1])  # select <equipment>...</equipment> only
    lines.extend(repr(xml3).splitlines()[2:-1])  # select <equipment>...</equipment> only
    lines.extend(repr(xml4).splitlines()[2:])  # skip XML declaration and <register>

    combined = xml()
    combined.source = '\n'.join(lines)
    assert combined.is_valid()


def test_not_unique(xml):
    xml1 = xml()
    xml1.id('MSLE.L.001')
    xml2 = xml()
    xml2.id('MSLE.L.002')
    xml3 = xml()
    xml3.id('MSLE.L.003')
    xml4 = xml()
    xml4.id('MSLE.L.002')

    lines = repr(xml1).splitlines()[1:-1]  # skip XML declaration and </register>
    lines.extend(repr(xml2).splitlines()[2:-1])  # select <equipment>...</equipment> only
    lines.extend(repr(xml3).splitlines()[2:-1])  # select <equipment>...</equipment> only
    lines.extend(repr(xml4).splitlines()[2:])  # skip XML declaration and <register>

    combined = xml()
    combined.source = '\n'.join(lines)
    combined.raises(r"Duplicate key-sequence \['MSLE.L.002'\]")
