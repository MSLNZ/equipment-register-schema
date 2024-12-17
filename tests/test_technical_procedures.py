import pytest


def test_empty(xml):
    xml.quality_manual('<technicalProcedures/>')
    assert xml.is_valid()


def test_multiple(xml):
    xml.quality_manual('<technicalProcedures/><technicalProcedures/>')
    xml.raises(r"technicalProcedures': This element is not expected")


def test_no_attributes_allowed(xml):
    xml.quality_manual(xml.element('technicalProcedures', x=1))
    xml.raises(r"attribute 'x' is not allowed")


def test_no_content(xml):
    xml.quality_manual(xml.element('technicalProcedures', text='content'))
    xml.raises(r'content other than whitespace is not allow')


def test_unexpected_child(xml):
    xml.quality_manual('<technicalProcedures><data>MSLT.L.0</data></technicalProcedures>')
    xml.raises(r"data': This element is not expected")


def test_unexpected_intermixed_child(xml):
    xml.quality_manual('<technicalProcedures>'
                       '  <id>MSLT.L.0</id>'
                       '  <data>MSLT.L.0</data>'
                       '</technicalProcedures>')
    xml.raises(r"data': This element is not expected")


def test_child_no_attributes(xml):
    xml.quality_manual('<technicalProcedures><id x="1">MSL</id></technicalProcedures>')
    xml.raises(r"attribute 'x' is not allowed")


@pytest.mark.parametrize(
    'value',
    ['MSLT.L.0',
     'MSLT.L.000000000000000000001',
     'MSLT.L.9876543210',
     'MSLT.L.0.0',
     'MSLT.L.000000001.1234567890',
     ])
def test_valid_id(xml, value):
    xml.quality_manual(f'<technicalProcedures><id>{value}</id></technicalProcedures>')
    assert xml.is_valid()


@pytest.mark.parametrize(
    'value',
    [' MSLT.L.0',
     ' MSLT.L.0.0',
     'MSLT.L.0 ',
     'MSLT.L.',
     'MSLT.L.0.0 ',
     'MSLX.L.0',
     'MsLT.L.0',
     'MSLT.Z.0',
     'MSLT0.0',
     'MSLT.0.0',
     'MSLT.0',
     'MSLT.L.a',
     'MSLT.L.0.a',
     'MSLT.L.08161f51419',
     'MSLT.L.0.08161f51419',
     'MSLT.L.0.',
     'MSLT.L.0. ',
     'nope',
     '123.4',
     '\nMSLT.L.001.048',
     'MSLT.L.001.048\n',
     'MSLT..L.001.048',
     'MSLT.L..001.048',
     'MSLT.L.001..048',
     'MSLT.L.001,048',
     'MSLT,L,001,048',
     'MSLT.L-001.048',
     ])
def test_invalid_id(xml, value):
    xml.quality_manual(f'<technicalProcedures><id>{value}</id></technicalProcedures>')
    xml.raises(r"not accepted by the pattern")


def test_multiple_id(xml):
    # ID's don't need to be unique
    e = xml.element('id', text='MSLT.L.0')
    xml.quality_manual(f'<technicalProcedures>{e}{e}{e}{e}{e}</technicalProcedures>')
    assert xml.is_valid()
