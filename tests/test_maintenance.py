import pytest


def test_invalid_name(xml):
    xml.maintenance('<invalid/>')
    xml.raises(r'Expected is .*maintenance')


def test_invalid_attribute(xml):
    xml.maintenance('<maintenance invalid="1"/>')
    xml.raises("maintenance', attribute 'invalid'")


@pytest.mark.parametrize(
    'value',
    ['',
     '   ',
     '2023',
     '2023-05',
     '2023-24-05',
     '23-24-05',
     '05-24-2023',
     '24-05-2023',
     'text',
     '24 May 2023',
     ])
def test_invalid_attribute_value(xml, value):
    xml.maintenance(f'<maintenance due="{value}"/>')
    xml.raises('not a valid value of the atomic type')


@pytest.mark.parametrize('value', ['2023-05-24', '2100-01-01'])
def test_valid_attribute_value(xml, value):
    xml.maintenance(f'<maintenance due="{value}"/>')
    assert xml.is_valid()


def test_invalid_subelement_name(xml):
    xml.maintenance('<maintenance><invalid/></maintenance>')
    xml.raises(r'Expected is .*task')


def test_task_date_missing(xml):
    xml.maintenance('<maintenance><task/></maintenance>')
    xml.raises("attribute 'date' is required")


def test_invalid_task_attribute_name(xml):
    xml.maintenance('<maintenance><task invalid="2023-06-14"/></maintenance>')
    xml.raises("task', attribute 'invalid'")


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
    xml.raises(r'Expected is .*task')


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
    xml.raises("task', attribute 'invalid'")
