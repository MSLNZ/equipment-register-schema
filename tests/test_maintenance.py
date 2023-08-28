import pytest


def test_invalid_name(xml):
    xml.maintenance('<invalid/>')
    xml.raises(r'Expected is \( .*maintenance \)')


def test_invalid_attribute(xml):
    xml.maintenance('<maintenance invalid="1"/>')
    xml.raises("The attribute 'invalid' is not allowed")


@pytest.mark.parametrize(
    'period',
    ['0.0e0', '1e2', '-2e-5'])
def test_invalid_period_value(xml, period):
    xml.maintenance(f'<maintenance period="{period}"/>')
    xml.raises('not a valid value of the atomic type')


@pytest.mark.parametrize(
    'period',
    [0, '0.0000', 1, 2.000000000000, 12678967.543233, 123456789])
def test_valid_period_value(xml, period):
    xml.maintenance(f'<maintenance period="{period}"/>')
    assert xml.is_valid()


@pytest.mark.parametrize(
    'period',
    [-0.001, -1, -1.00000, -99, -100000])
def test_negative_period_value(xml, period):
    xml.maintenance(f'<maintenance period="{period}"/>')
    xml.raises(r"minimum value allowed \('0'\)")


def test_invalid_subelement_name(xml):
    xml.maintenance('<maintenance><invalid/></maintenance>')
    xml.raises(r'Expected is \( .*task \)')


def test_task_date_missing(xml):
    xml.maintenance('<maintenance><task/></maintenance>')
    xml.raises("attribute 'date' is required")


def test_invalid_task_attribute_name(xml):
    xml.maintenance('<maintenance><task invalid="2023-06-14"/></maintenance>')
    xml.raises("attribute 'invalid' is not allowed")


def test_invalid_task_attribute_value(xml):
    xml.maintenance('<maintenance><task date="14 June 2023"/></maintenance>')
    xml.raises("atomic type 'xs:date'")


@pytest.mark.parametrize(
    'text',
    ['',
     ' ',
     '       ',
     '\t',
     '\t         ',
     '\r',
     '\n',
     ' \t\n \r ',
     'Replaced\nthe diode',
     'Replaced\nthe\tdiode',
     'Replaced\rthe diode',
     'Replaced\rthe\tdiode',
     ])
def test_invalid_task_pattern(xml, text):
    xml.maintenance(f'<maintenance><task date="2023-06-14">{text}</task></maintenance>')
    xml.raises('not accepted by the pattern')


@pytest.mark.parametrize(
    'text',
    ['a',
     ' a',
     'a ',
     '  a     ',
     'Replaced the diode',
     ' Replaced the    diode',
     'Replaced\tthe\tdiode',
     'The diode (model xxx) died and therefore it was replace with a newer model (yyy)'
     ])
def test_valid_task_pattern(xml, text):
    xml.maintenance(f'<maintenance><task date="2023-06-14">{text}</task></maintenance>')
    assert xml.is_valid()


def test_multiple_tasks_all_valid(xml):
    xml.maintenance(f'<maintenance>'
                    f'  <task date="2023-06-19">Fix something</task>'
                    f'  <task date="2023-06-18">Fix something</task>'
                    f'  <task date="2023-06-17">Fix something</task>'
                    f'  <task date="2023-06-16">Fix something</task>'
                    f'  <task date="2023-06-15">Fix something</task>'
                    f'</maintenance>')
    assert xml.is_valid()


def test_multiple_tasks_invalid_text(xml):
    xml.maintenance(f'<maintenance>'
                    f'  <task date="2023-06-19">Fix something</task>'
                    f'  <task date="2023-06-18">Fix something</task>'
                    f'  <task date="2023-06-17"></task>'
                    f'  <task date="2023-06-16">Fix something</task>'
                    f'  <task date="2023-06-15">Fix something</task>'
                    f'</maintenance>')
    xml.raises('not accepted by the pattern')


def test_multiple_tasks_invalid_name(xml):
    xml.maintenance(f'<maintenance>'
                    f'  <task date="2023-06-19">Fix something</task>'
                    f'  <task date="2023-06-18">Fix something</task>'
                    f'  <task date="2023-06-17">Fix something</task>'
                    f'  <invalid date="2023-06-16">Fix something</invalid>'
                    f'  <task date="2023-06-15">Fix something</task>'
                    f'</maintenance>')
    xml.raises(r'Expected is \( .*task \)')


def test_multiple_tasks_invalid_attribute_value(xml):
    xml.maintenance(f'<maintenance>'
                    f'  <task date="2023-06-19">Fix something</task>'
                    f'  <task date="2023-06-18">Fix something</task>'
                    f'  <task date="17-06-2023">Fix something</task>'
                    f'  <task date="2023-06-16">Fix something</task>'
                    f'  <task date="2023-06-15">Fix something</task>'
                    f'</maintenance>')
    xml.raises("atomic type 'xs:date'")


def test_multiple_tasks_invalid_attribute_name(xml):
    xml.maintenance(f'<maintenance>'
                    f'  <task date="2023-06-19">Fix something</task>'
                    f'  <task date="2023-06-18">Fix something</task>'
                    f'  <task date="2023-06-17">Fix something</task>'
                    f'  <task date="2023-06-16">Fix something</task>'
                    f'  <task invalid="2023-06-15">Fix something</task>'
                    f'</maintenance>')
    xml.raises("The attribute 'invalid' is not allowed")
