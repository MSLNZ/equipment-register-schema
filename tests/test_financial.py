import pytest

from .conftest import INVALID_DATES

unexpected = "<unexpected>text</unexpected>"
purchase = "<purchaseYear>2020</purchaseYear>"
warranty = "<warrantyExpirationDate>2025-08-15</warrantyExpirationDate>"
capex = (
    "<capitalExpenditure>"
    "<assetNumber/>"
    "<depreciationEndYear>2030</depreciationEndYear>"
    '<price currency="NZD">10000</price>'
    "</capitalExpenditure>"
)


def test_empty(xml) -> None:
    xml.quality_manual("<financial/>")
    assert xml.is_valid()


def test_multiple(xml):
    xml.quality_manual("<financial/><financial/>")
    xml.raises(r"financial': This element is not expected")


@pytest.mark.parametrize(
    "asset", ["", " \n \t   ", "01234", "ABC123", ":any-\n@thing "]
)
def test_asset_number_valid(xml, asset):
    f = (
        f"<financial>"
        f"  <capitalExpenditure>"
        f"    <assetNumber>{asset}</assetNumber>"
        f"    <depreciationEndYear>2030</depreciationEndYear>"
        f'    <price currency="NZD">10000</price>'
        f"  </capitalExpenditure>"
        f"</financial>"
    )
    xml.quality_manual(f)
    assert xml.is_valid()


def test_asset_number_repeated(xml):
    f = (
        "<financial>"
        "  <capitalExpenditure>"
        "    <assetNumber/>"
        "    <depreciationEndYear>2030</depreciationEndYear>"
        '    <price currency="NZD">10000</price>'
        "    <assetNumber/>"
        "  </capitalExpenditure>"
        "</financial>"
    )
    xml.quality_manual(f)
    xml.raises(r"assetNumber': This element is not expected")


def test_capex_order_invalid_1(xml):
    f = (
        "<financial>"
        "  <capitalExpenditure>"
        "    <depreciationEndYear>2030</depreciationEndYear>"
        '    <price currency="NZD">10000</price>'
        "    <assetNumber/>"
        "  </capitalExpenditure>"
        "</financial>"
    )
    xml.quality_manual(f)
    xml.raises(r"depreciationEndYear': This element is not expected")


def test_capex_order_invalid_2(xml):
    f = (
        "<financial>"
        "  <capitalExpenditure>"
        "    <assetNumber/>"
        '    <price currency="NZD">10000</price>'
        "    <depreciationEndYear>2030</depreciationEndYear>"
        "  </capitalExpenditure>"
        "</financial>"
    )
    xml.quality_manual(f)
    xml.raises(r"price': This element is not expected")


def test_price_currency_invalid(xml):
    f = (
        "<financial>"
        "  <capitalExpenditure>"
        "    <assetNumber/>"
        "    <depreciationEndYear>2030</depreciationEndYear>"
        '    <price currency="ABC">10000</price>'
        "  </capitalExpenditure>"
        "</financial>"
    )
    xml.quality_manual(f)
    xml.raises(r"ABC' is not an element of the set")


@pytest.mark.parametrize("price", ["0", "150000", "150e3", "150000.00"])
def test_price_valid(xml, price):
    f = (
        f"<financial>"
        f"  <capitalExpenditure>"
        f"    <assetNumber/>"
        f"    <depreciationEndYear>2030</depreciationEndYear>"
        f'    <price currency="NZD">{price}</price>'
        f"  </capitalExpenditure>"
        f"</financial>"
    )
    xml.quality_manual(f)
    assert xml.is_valid()


@pytest.mark.parametrize("price", ["", "  \n ", "150k"])
def test_price_invalid(xml, price):
    f = (
        f"<financial>"
        f"  <capitalExpenditure>"
        f"    <assetNumber/>"
        f"    <depreciationEndYear>2030</depreciationEndYear>"
        f'    <price currency="NZD">{price}</price>'
        f"  </capitalExpenditure>"
        f"</financial>"
    )
    xml.quality_manual(f)
    xml.raises(r"not a valid value of the atomic type 'xs:float'")


def test_warranty_date_valid(xml):
    xml.quality_manual(f"<financial>{warranty}</financial>")
    assert xml.is_valid()


@pytest.mark.parametrize("date", INVALID_DATES)
def test_warranty_date_invalid(xml, date):
    f = f"<financial><warrantyExpirationDate>{date}</warrantyExpirationDate></financial>"
    xml.quality_manual(f)
    xml.raises(r"atomic type 'xs:date'")


def test_year_purchased_valid(xml):
    xml.quality_manual(f"<financial>{purchase}</financial>")
    assert xml.is_valid()


@pytest.mark.parametrize("year", ["202", "1", "", "two"])
def test_year_purchased_invalid(xml, year):
    f = f"<financial><purchaseYear>{year}</purchaseYear></financial>"
    xml.quality_manual(f)
    xml.raises(r"atomic type 'xs:gYear'")


@pytest.mark.parametrize(
    "children",
    [
        f"{purchase}{warranty}{capex}",
        f"{purchase}{capex}{warranty}",
        f"{capex}{warranty}{purchase}",
        f"{capex}{purchase}{warranty}",
        f"{warranty}{capex}{purchase}",
        f"{warranty}{purchase}{capex}",
    ],
)
def test_any_order_valid(xml, children):
    xml.quality_manual(f"<financial>{children}</financial>")
    assert xml.is_valid()


@pytest.mark.parametrize(
    "children",
    [
        f"{unexpected}",
        f"{purchase}{unexpected}",
        f"{warranty}{unexpected}",
        f"{capex}{unexpected}",
        f"{purchase}{warranty}{unexpected}",
        f"{warranty}{purchase}{capex}{unexpected}",
    ],
)
def test_unexpected_element(xml, children):
    xml.quality_manual(f"<financial>{children}</financial>")
    xml.raises(r"unexpected': This element is not expected")


@pytest.mark.parametrize(
    "children",
    [
        f"{warranty}{warranty}",
        f"{warranty}{capex}{warranty}",
    ],
)
def test_warranty_repeated(xml, children):
    xml.quality_manual(f"<financial>{children}</financial>")
    xml.raises(r"warrantyExpirationDate': This element is not expected")


@pytest.mark.parametrize(
    "children",
    [
        f"{purchase}{purchase}",
        f"{purchase}{capex}{purchase}",
    ],
)
def test_year_purchased_repeated(xml, children):
    xml.quality_manual(f"<financial>{children}</financial>")
    xml.raises(r"purchaseYear': This element is not expected")
