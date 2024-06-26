import pytest

from tests.conftest import INVALID_DATES


def test_invalid_name(xml):
    xml.maintenance('<invalid/>')
    xml.raises(r'Expected is .*maintenance')


def test_repeated(xml):
    xml.maintenance('<maintenance/><maintenance/>')
    xml.raises(r'Expected is .*firmware')


def test_invalid_attribute(xml):
    xml.maintenance('<maintenance invalid="1"/>')
    xml.raises("maintenance', attribute 'invalid'")


def test_valid_attributes(xml):
    xml.maintenance(f'<maintenance dueDate="2023-05-24" serviceAgent="Company X"/>')
    assert xml.is_valid()


@pytest.mark.parametrize('value', INVALID_DATES)
def test_invalid_due_date_value(xml, value):
    xml.maintenance(f'<maintenance dueDate="{value}"/>')
    xml.raises('not a valid value of the atomic type')


@pytest.mark.parametrize('value', ['2023-05-24', '2100-01-01'])
def test_valid_due_date_value(xml, value):
    xml.maintenance(f'<maintenance dueDate="{value}"/>')
    assert xml.is_valid()


@pytest.mark.parametrize('value', ['', 'MSL-Electrical', 'External Company ABC Inc.'])
def test_valid_service_agent(xml, value):
    xml.maintenance(f'<maintenance serviceAgent="{value}"/>')
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


@pytest.mark.parametrize('value', INVALID_DATES)
def test_invalid_task_attribute_value(xml, value):
    xml.maintenance(f'<maintenance><task date="{value}"/></maintenance>')
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
    xml.maintenance('<maintenance>'
                    '  <task date="2023-06-19">Fix something</task>'
                    '  <task date="2023-06-18">Fix something</task>'
                    '  <task date="2023-06-17">Fix something</task>'
                    '  <task date="2023-06-16">Fix something</task>'
                    '  <task date="2023-06-15">Fix something</task>'
                    '</maintenance>')
    assert xml.is_valid()


def test_multiple_tasks_invalid_text(xml):
    xml.maintenance('<maintenance>'
                    '  <task date="2023-06-19">Fix something</task>'
                    '  <task date="2023-06-18">Fix something</task>'
                    '  <task date="2023-06-17"></task>'
                    '  <task date="2023-06-16">Fix something</task>'
                    '  <task date="2023-06-15">Fix something</task>'
                    '</maintenance>')
    xml.raises('not accepted by the pattern')


def test_multiple_tasks_invalid_name(xml):
    xml.maintenance('<maintenance>'
                    '  <task date="2023-06-19">Fix something</task>'
                    '  <task date="2023-06-18">Fix something</task>'
                    '  <task date="2023-06-17">Fix something</task>'
                    '  <invalid date="2023-06-16">Fix something</invalid>'
                    '  <task date="2023-06-15">Fix something</task>'
                    '</maintenance>')
    xml.raises(r'Expected is .*task')


@pytest.mark.parametrize('value', INVALID_DATES)
def test_multiple_tasks_invalid_attribute_value(xml, value):
    xml.maintenance(f'<maintenance>'
                    f'  <task date="2023-06-19">Fix something</task>'
                    f'  <task date="2023-06-18">Fix something</task>'
                    f'  <task date="{value}">Fix something</task>'
                    f'  <task date="2023-06-16">Fix something</task>'
                    f'  <task date="2023-06-15">Fix something</task>'
                    f'</maintenance>')
    xml.raises("atomic type 'xs:date'")


def test_multiple_tasks_invalid_attribute_name(xml):
    xml.maintenance('<maintenance>'
                    '  <task date="2023-06-19">Fix something</task>'
                    '  <task date="2023-06-18">Fix something</task>'
                    '  <task date="2023-06-17">Fix something</task>'
                    '  <task date="2023-06-16">Fix something</task>'
                    '  <task invalid="2023-06-15">Fix something</task>'
                    '</maintenance>')
    xml.raises("task', attribute 'invalid'")
