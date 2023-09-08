def test_subelement_invalid_name(xml):
    xml.calibrations(xml.measurand('<invalid/>'))
    xml.raises(r'Expected is \( .*report \)')


def test_default_one_report(xml):
    xml.calibrations(xml.measurand(xml.report()))
    assert xml.is_valid()


def test_default_two_reports(xml):
    r1 = xml.report()
    r2 = xml.report()
    xml.calibrations(xml.measurand(f'{r1}\n  {r2}'))
    assert xml.is_valid()
