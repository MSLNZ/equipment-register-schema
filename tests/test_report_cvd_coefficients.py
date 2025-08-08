import pytest


def test_missing_children(xml):
    choice = "<cvdCoefficients/>"
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises("Missing child element")


def test_expect_r0(xml):
    choice = "<cvdCoefficients>  <invalid/></cvdCoefficients>"
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r"Expected is .*R0")


@pytest.mark.parametrize("r0", ["", "one hundred", "1.000189e+02", "3.f0"])
def test_r0_value_invalid_syntax(xml, r0):
    choice = f"<cvdCoefficients>  <R0>{r0}</R0></cvdCoefficients>"
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r"not a valid value of the atomic type .+nonNegativeDecimal")


def test_r0_value_negative(xml):
    choice = f"<cvdCoefficients>  <R0>-1</R0></cvdCoefficients>"
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r"value '-1' is less than the minimum value allowed")


def test_r0_does_not_accept_attributes(xml):
    choice = '<cvdCoefficients>  <R0 variables="t">100</R0></cvdCoefficients>'
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r"attribute 'variables' is not allowed")


def test_expect_capital_a(xml):
    choice = "<cvdCoefficients>  <R0>100</R0>  <a>1</a></cvdCoefficients>"
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r"Expected is .*A")


@pytest.mark.parametrize("a", ["", "one hundred", "3.f0"])
def test_a_value_invalid(xml, a):
    choice = f"<cvdCoefficients>  <R0>100</R0>  <A>{a}</A></cvdCoefficients>"
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r"not a valid value of the atomic type 'xs:double'")


def test_a_does_not_accept_attributes(xml):
    choice = '<cvdCoefficients>  <R0>100</R0>  <A variables="t">1</A></cvdCoefficients>'
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r"attribute 'variables' is not allowed")


def test_expect_capital_b(xml):
    choice = "<cvdCoefficients>  <R0>100</R0>  <A>1</A></cvdCoefficients>"
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r"Expected is .*B")


@pytest.mark.parametrize("b", ["", "one hundred", "3.f0"])
def test_b_value_invalid(xml, b):
    choice = f"<cvdCoefficients>  <R0>100</R0>  <A>1</A>  <B>{b}</B></cvdCoefficients>"
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r"not a valid value of the atomic type 'xs:double'")


def test_b_does_not_accept_attributes(xml):
    choice = (
        "<cvdCoefficients>"
        "  <R0>100</R0>"
        "  <A>1</A>"
        '  <B variables="t">1</B>'
        "</cvdCoefficients>"
    )
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r"attribute 'variables' is not allowed")


def test_expect_capital_c(xml):
    choice = (
        "<cvdCoefficients>"
        "  <R0>100</R0>"
        "  <A>1</A>"
        "  <B>1</B>"
        "  <B>1</B>"
        "</cvdCoefficients>"
    )
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r"Expected is .*C")


@pytest.mark.parametrize("c", ["", "one hundred", "3.f0"])
def test_c_value_invalid(xml, c):
    choice = (
        f"<cvdCoefficients>"
        f"  <R0>100</R0>"
        f"  <A>1</A>"
        f"  <B>1</B>"
        f"  <C>{c}</C>"
        f"</cvdCoefficients>"
    )
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r"not a valid value of the atomic type 'xs:double'")


def test_c_does_not_accept_attributes(xml):
    choice = (
        "<cvdCoefficients>"
        "  <R0>100</R0>"
        "  <A>1</A>"
        "  <B>1</B>"
        '  <C variables="t">1</C>'
        "</cvdCoefficients>"
    )
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r"attribute 'variables' is not allowed")


def test_expect_uncertainty(xml):
    choice = (
        "<cvdCoefficients>"
        "  <R0>100</R0>"
        "  <A>1</A>"
        "  <B>1</B>"
        "  <C>1</C>"
        "</cvdCoefficients>"
    )
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r"Expected is .*uncertainty")


def test_missing_uncertainty_variables_attribute(xml):
    choice = (
        "<cvdCoefficients>"
        "  <R0>100</R0>"
        "  <A>1</A>"
        "  <B>1</B>"
        "  <C>1</C>"
        "  <uncertainty>0.2</uncertainty>"
        "</cvdCoefficients>"
    )
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r"attribute \'variables\'")


def test_wrong_uncertainty_attribute_name(xml):
    choice = (
        "<cvdCoefficients>"
        "  <R0>100</R0>"
        "  <A>1</A>"
        "  <B>1</B>"
        "  <C>1</C>"
        '  <uncertainty apple="red">0.2</uncertainty>'
        "</cvdCoefficients>"
    )
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r"attribute \'apple\'")


def test_extra_uncertainty_attribute(xml):
    choice = (
        "<cvdCoefficients>"
        "  <R0>100</R0>"
        "  <A>1</A>"
        "  <B>1</B>"
        "  <C>1</C>"
        '  <uncertainty variables="" save="true">0.2</uncertainty>'
        "</cvdCoefficients>"
    )
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r"attribute \'save\'")


def test_uncertainty_as_equation(xml):
    choice = (
        "<cvdCoefficients>"
        "  <R0>100</R0>"
        "  <A>1</A>"
        "  <B>1</B>"
        "  <C>1</C>"
        '  <uncertainty variables="">0.2/2.1</uncertainty>'
        "  <range><minimum>0</minimum><maximum>100</maximum></range>"
        "</cvdCoefficients>"
    )
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    assert xml.is_valid()


def test_expect_range_element(xml):
    choice = (
        "<cvdCoefficients>"
        "  <R0>100</R0>"
        "  <A>1</A>"
        "  <B>1</B>"
        "  <C>1</C>"
        '  <uncertainty variables="">0.2/2.1</uncertainty>'
        "  <ranges/>"
        "</cvdCoefficients>"
    )
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r"Expected is .*range")


def test_expect_degree_freedom_element(xml):
    choice = (
        "<cvdCoefficients>"
        "  <R0>100</R0>"
        "  <A>1</A>"
        "  <B>1</B>"
        "  <C>1</C>"
        '  <uncertainty variables="">0.2/2.1</uncertainty>'
        '  <range><minimum>0</minimum><maximum>100</maximum></range>'
        "  <invalid>3*x+1</invalid>"
        "</cvdCoefficients>"
    )
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r"Expected is .*degreeFreedom")


def test_degree_freedom_optional(xml):
    choice = (
        "<cvdCoefficients>"
        "  <R0>100</R0>"
        "  <A>1</A>"
        "  <B>1</B>"
        "  <C>1</C>"
        '  <uncertainty variables="">0.2/2.1</uncertainty>'
        "  <range><minimum>0</minimum><maximum>100</maximum></range>"
        "</cvdCoefficients>"
    )
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    assert xml.is_valid()


def test_range_expect_minimum(xml):
    choice = (
        '<cvdCoefficients>'
        '  <R0>100</R0>'
        '  <A>1</A>'
        '  <B>1</B>'
        '  <C>1</C>'
        '  <uncertainty variables="">0.2/2.1</uncertainty>'
        '  <range/>'
        '</cvdCoefficients>'
    )
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises('Expected is .+minimum')


def test_range_expect_maximum(xml):
    choice = (
        '<cvdCoefficients>'
        '  <R0>100</R0>'
        '  <A>1</A>'
        '  <B>1</B>'
        '  <C>1</C>'
        '  <uncertainty variables="">0.2/2.1</uncertainty>'
        '  <range>'
        '    <minimum>1</minimum>'
        '  </range>'
        '</cvdCoefficients>'
    )
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises('Expected is .+maximum')


def test_range_unexpected(xml):
    choice = (
        '<cvdCoefficients>'
        '  <R0>100</R0>'
        '  <A>1</A>'
        '  <B>1</B>'
        '  <C>1</C>'
        '  <uncertainty variables="">0.2/2.1</uncertainty>'
        '  <range>'
        '    <minimum>1</minimum>'
        '    <maximum>1</maximum>'
        '    <extra>1</extra>'
        '  </range>'
        '</cvdCoefficients>'
    )
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises("extra': This element is not expected")


def test_range_no_attributes(xml):
    choice = (
        '<cvdCoefficients>'
        '  <R0>100</R0>'
        '  <A>1</A>'
        '  <B>1</B>'
        '  <C>1</C>'
        '  <uncertainty variables="">0.2/2.1</uncertainty>'
        '  <range variable="t">'
        '    <minimum>1</minimum>'
        '    <maximum>1</maximum>'
        '  </range>'
        '</cvdCoefficients>'
    )
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises("attribute 'variable' is not allowed")


def test_range_invalid_minimum(xml):
    choice = (
        "<cvdCoefficients>"
        "  <R0>100</R0>"
        "  <A>1</A>"
        "  <B>1</B>"
        "  <C>1</C>"
        '  <uncertainty variables="">0.2/2.1</uncertainty>'
        '  <range>'
        "    <minimum>A</minimum>"
        "  </range>"
        "</cvdCoefficients>"
    )
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises("not a valid value of the atomic type 'xs:double'")


def test_range_invalid_maximum(xml):
    choice = (
        '<cvdCoefficients>'
        '  <R0>100</R0>'
        '  <A>1</A>'
        '  <B>1</B>'
        '  <C>1</C>'
        '  <uncertainty variables="">0.2/2.1</uncertainty>'
        '  <range>'
        '    <minimum>1</minimum>'
        '    <maximum>A</maximum>'
        '  </range>'
        '</cvdCoefficients>'
    )
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises("not a valid value of the atomic type 'xs:double'")


def test_element_after_degree_freedom(xml):
    choice = (
        '<cvdCoefficients>'
        '  <R0>100</R0>'
        '  <A>1</A>'
        '  <B>1</B>'
        '  <C>1</C>'
        '  <uncertainty variables="">0.2/2.1</uncertainty>'
        '  <range>'
        '    <minimum>1</minimum>'
        '    <maximum>10</maximum>'
        '  </range>'
        '  <degreeFreedom>1</degreeFreedom>'
        '  <extra>1</extra>'
        '</cvdCoefficients>'
    )
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises("extra': This element is not expected")


def test_degree_freedom_invalid(xml):
    choice = (
        '<cvdCoefficients>'
        '  <R0>100</R0>'
        '  <A>1</A>'
        '  <B>1</B>'
        '  <C>1</C>'
        '  <uncertainty variables="">0.2/2.1</uncertainty>'
        '  <range>'
        '    <minimum>1</minimum>'
        '    <maximum>10</maximum>'
        '  </range>'
        '  <degreeFreedom>-1</degreeFreedom>'
        '</cvdCoefficients>'
    )
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises("value '-1' is less than the minimum value allowed")
