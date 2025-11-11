from lxml import etree
import pytest


@pytest.mark.parametrize(
    "name",
    [
        "currencyEnumerationString",
        "digitalFormatEnumerationString",
        "keywordsList",
        "labEnumerationString",
        "quantityEnumerationString",
        "staffEnumerationString",
        "statusEnumerationString",
        "teamEnumerationString",
    ],
)
def test_enumerations(name: str) -> None:
    # make sure the enum values are in alphabetical order (case insensitive)
    tree = etree.parse("equipment-register.xsd")

    restrictions = tree.xpath(
        f"./xsd:simpleType[@name={name!r}]//xsd:restriction",
        namespaces={"xsd": "http://www.w3.org/2001/XMLSchema"},
    )

    assert len(restrictions) == 1

    values = [element.attrib["value"] for element in restrictions[0]]
    assert sorted(values, key=str.casefold) == values
