import pytest

from .conftest import INVALID_DATES

unexpected = "<unexpected>text</unexpected>"
purchase = "<purchaseYear>2020</purchaseYear>"
warranty = "<warrantyExpirationDate>2025-08-15</warrantyExpirationDate>"
capex = (
    "<capitalExpenditure>"
    "<assetNumber/>"
    "<depreciationStartDate>2020-02-10</depreciationStartDate>"
    '<price currency="NZD">10000</price>'
    "<usefulLife>10</usefulLife>"
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
def test_capex_asset_number_valid(xml, asset):
    f = (
        f"<financial>"
        f"  <capitalExpenditure>"
        f"    <assetNumber>{asset}</assetNumber>"
        f"    <depreciationStartDate>2020-02-10</depreciationStartDate>"
        f'    <price currency="NZD">10000</price>'
        f"    <usefulLife>10</usefulLife>"
        f"  </capitalExpenditure>"
        f"</financial>"
    )
    xml.quality_manual(f)
    assert xml.is_valid()


def test_capex_asset_number_repeated(xml):
    f = (
        "<financial>"
        "  <capitalExpenditure>"
        "    <assetNumber/>"
        "    <depreciationStartDate>2020-02-10</depreciationStartDate>"
        '    <price currency="NZD">10000</price>'
        "    <usefulLife>10</usefulLife>"
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
        "    <depreciationStartDate>2020-02-10</depreciationStartDate>"
        '    <price currency="NZD">10000</price>'
        "    <usefulLife>10</usefulLife>"
        "    <assetNumber/>"
        "  </capitalExpenditure>"
        "</financial>"
    )
    xml.quality_manual(f)
    xml.raises(r"depreciationStartDate': This element is not expected")


def test_capex_order_invalid_2(xml):
    f = (
        "<financial>"
        "  <capitalExpenditure>"
        "    <assetNumber/>"
        '    <price currency="NZD">10000</price>'
        "    <usefulLife>10</usefulLife>"
        "    <depreciationStartDate>2020-02-10</depreciationStartDate>"
        "  </capitalExpenditure>"
        "</financial>"
    )
    xml.quality_manual(f)
    xml.raises(r"price': This element is not expected")

def test_capex_order_invalid_3(xml):
    f = (
        "<financial>"
        "  <capitalExpenditure>"
        "    <assetNumber/>"
        "    <depreciationStartDate>2020-02-10</depreciationStartDate>"
        "    <usefulLife>10</usefulLife>"
        '    <price currency="NZD">10000</price>'
        "  </capitalExpenditure>"
        "</financial>"
    )
    xml.quality_manual(f)
    xml.raises(r"usefulLife': This element is not expected")

@pytest.mark.parametrize("date", INVALID_DATES)
def test_capex_depreciation_invalid_date(xml, date):
    f = (
        "<financial>"
        "  <capitalExpenditure>"
        "    <assetNumber/>"
        f"    <depreciationStartDate>{date}</depreciationStartDate>"
        '    <price currency="NZD">10000</price>'
        "    <usefulLife>10</usefulLife>"
        "  </capitalExpenditure>"
        "</financial>"
    )
    xml.quality_manual(f)
    xml.raises(r"depreciationStartDate':")

def test_capex_price_currency_missing(xml):
    f = (
        "<financial>"
        "  <capitalExpenditure>"
        "    <assetNumber/>"
        "    <depreciationStartDate>2020-02-10</depreciationStartDate>"
        '    <price>10000</price>'
        "    <usefulLife>10</usefulLife>"
        "  </capitalExpenditure>"
        "</financial>"
    )
    xml.quality_manual(f)
    xml.raises(r"attribute 'currency' is required")


def test_capex_price_currency_invalid(xml):
    f = (
        "<financial>"
        "  <capitalExpenditure>"
        "    <assetNumber/>"
        "    <depreciationStartDate>2020-02-10</depreciationStartDate>"
        '    <price currency="ABC">10000</price>'
        "    <usefulLife>10</usefulLife>"
        "  </capitalExpenditure>"
        "</financial>"
    )
    xml.quality_manual(f)
    xml.raises(r"ABC' is not an element of the set")


@pytest.mark.parametrize("price", ["0", "150000", "150e3", "150000.00"])
def test_capex_price_valid(xml, price):
    f = (
        f"<financial>"
        f"  <capitalExpenditure>"
        f"    <assetNumber/>"
        "    <depreciationStartDate>2020-02-10</depreciationStartDate>"
        f'    <price currency="NZD">{price}</price>'
        "    <usefulLife>10</usefulLife>"
        f"  </capitalExpenditure>"
        f"</financial>"
    )
    xml.quality_manual(f)
    assert xml.is_valid()


@pytest.mark.parametrize("price", ["", "  \n ", "150k"])
def test_capex_price_invalid(xml, price):
    f = (
        f"<financial>"
        f"  <capitalExpenditure>"
        f"    <assetNumber/>"
        "    <depreciationStartDate>2020-02-10</depreciationStartDate>"
        f'    <price currency="NZD">{price}</price>'
        "    <usefulLife>10</usefulLife>"
        f"  </capitalExpenditure>"
        f"</financial>"
    )
    xml.quality_manual(f)
    xml.raises(r"not a valid value of the atomic type 'xs:float'")

@pytest.mark.parametrize("life", ["0", "8", "12.345", "100"])
def test_capex_useful_life_valid(xml, life):
    f = (
        f"<financial>"
        f"  <capitalExpenditure>"
        f"    <assetNumber/>"
        "    <depreciationStartDate>2020-02-10</depreciationStartDate>"
        '    <price currency="NZD">10000</price>'
        f"    <usefulLife>{life}</usefulLife>"
        f"  </capitalExpenditure>"
        f"</financial>"
    )
    xml.quality_manual(f)
    assert xml.is_valid()

@pytest.mark.parametrize("life", ["", "  \n ", "-1", "1e1"])
def test_capex_useful_life_invalid(xml, life):
    f = (
        "<financial>"
        "  <capitalExpenditure>"
        "    <assetNumber/>"
        "    <depreciationStartDate>2020-02-10</depreciationStartDate>"
        '    <price currency="NZD">10000</price>'
        f"    <usefulLife>{life}</usefulLife>"
        "  </capitalExpenditure>"
        "</financial>"
    )
    xml.quality_manual(f)
    xml.raises(r"usefulLife':")

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
