import pytest


@pytest.mark.parametrize(
    'content, attribs',
    [('', {}),
     ('   anything\n\n\n', {'foo': 'bar'}),
     ('{"x":1}', {'hello': 'world', 'y': "1"}),
     ])
def test_valid(xml, content, attribs):
    # not testing for a valid GTC-Archive string, this should be validated in Python
    choice = xml.element('gtcArchive', text=content, **attribs)
    xml.calibrations(xml.measurand(xml.report(choice=choice)))
    assert xml.is_valid()


def test_subelements_not_allowed(xml):
    choice = '<gtcArchive><child/></gtcArchive>'
    xml.calibrations(xml.measurand(xml.report(choice=choice)))
    xml.raises('Element content is not allowed')
