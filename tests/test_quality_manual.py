import pytest


def test_missing(xml):
    xml.quality_manual(None)
    xml.raises(r'Expected is .*qualityManual')


def test_empty(xml):
    xml.quality_manual('')
    assert xml.is_valid()


def test_no_content(xml):
    xml.quality_manual('hello')
    xml.raises(r'content other than whitespace is not allowed')


def test_no_attributes_allowed(xml):
    xml.quality_manual(hello='world')
    xml.raises(r"attribute 'hello' is not allowed")


@pytest.mark.parametrize(
    'body',
    ['<accessories/>',
     '<serviceAgent/>',
     '<financial/>',
     '<documentation/>',
     '<personnelRestrictions/>',
     '<technicalProcedures/>',
     '<financial/><accessories/>',
     '<financial/><personnelRestrictions/><accessories/><serviceAgent/><technicalProcedures/><documentation/>',
     '<personnelRestrictions/><technicalProcedures/><serviceAgent/>',
     ])
def test_any_child_order(xml, body):
    xml.quality_manual(body)
    assert xml.is_valid()


@pytest.mark.parametrize(
    'body',
    ['<hello/>',
     '<serviceAgent/><hello/>',
     '<financial/><accessories/><hello/>',
     '<financial/><personnelRestrictions/><accessories/><hello/><serviceAgent/><technicalProcedures/><documentation/>',
     '<personnelRestrictions/><technicalProcedures/><serviceAgent/><hello/>',
     ])
def test_unexpected_child_intermixed(xml, body):
    xml.quality_manual(body)
    xml.raises(r"hello': This element is not expected")
