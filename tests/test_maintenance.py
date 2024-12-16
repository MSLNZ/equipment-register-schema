import pytest

from tests.conftest import INVALID_DATES

INVALID_TASK_TEXT = [
    '',
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
]

VALID_TASK_TEXT = [
    'a',
    ' a',
    'a ',
    '  a     ',
    'Replace the diode',
    ' Replace the    diode',
    'Replace\tthe\tdiode',
    'The diode (model: xxx) is flaky and it should be replaced with a newer model (yyy)'
]


def test_invalid_name(xml):
    xml.maintenance('<invalid/>')
    xml.raises(r'Expected is .*maintenance')


def test_empty(xml):
    xml.maintenance('<maintenance/>')
    assert xml.is_valid()


def test_repeated(xml):
    xml.maintenance('<maintenance/><maintenance/>')
    xml.raises(r'Expected is .*alterations')


def test_no_top_level_attribute_allowed(xml):
    xml.maintenance('<maintenance dateDue="2024-10-10"/>')
    xml.raises("maintenance', attribute 'dateDue'")


@pytest.mark.parametrize('name', ['completed', 'invalid'])
def test_expect_planned_element(xml, name):
    xml.maintenance(f'<maintenance><{name}/></maintenance>')
    xml.raises(r'Expected is .*planned')


@pytest.mark.parametrize('name', ['planned', 'invalid'])
def test_expect_completed_element(xml, name):
    xml.maintenance(f'<maintenance><planned/><{name}/></maintenance>')
    xml.raises(r'Expected is .*completed')


@pytest.mark.parametrize('name', ['planned', 'completed', 'invalid'])
def test_unexpected_element(xml, name):
    xml.maintenance(f'<maintenance><planned/><completed/><{name}/></maintenance>')
    xml.raises(rf"{name}': This element is not expected")


def test_planned_no_attribute_allowed(xml):
    xml.maintenance(f'<maintenance><planned a="b"/><completed/></maintenance>')
    xml.raises(r"attribute 'a' is not allowed")


def test_completed_no_attribute_allowed(xml):
    xml.maintenance(f'<maintenance><planned/><completed a="b"/></maintenance>')
    xml.raises(r"attribute 'a' is not allowed")


def test_planned_invalid_subelement(xml):
    xml.maintenance('<maintenance>'
                    '  <planned>'
                    '    <event>Service laser</event>'
                    '  </planned>'
                    '  <completed/>'
                    '</maintenance>')
    xml.raises(r"event': This element is not expected")


def test_planned_task_date_due_missing(xml):
    xml.maintenance('<maintenance>'
                    '  <planned>'
                    '    <task>Service laser</task>'
                    '  </planned>'
                    '  <completed/>'
                    '</maintenance>')
    xml.raises(r"The attribute 'dateDue' is required but missing")


@pytest.mark.parametrize('text', INVALID_TASK_TEXT)
def test_planned_task_invalid_text(xml, text):
    xml.maintenance(f'<maintenance>'
                    f'  <planned>'
                    f'    <task dateDue="2024-10-10">{text}</task>'
                    f'  </planned>'
                    f'  <completed/>'
                    f'</maintenance>')
    xml.raises('not accepted by the pattern')


@pytest.mark.parametrize('date', INVALID_DATES)
def test_planned_task_invalid_date_due(xml, date):
    xml.maintenance(f'<maintenance>'
                    f'  <planned>'
                    f'    <task dateDue="{date}">Fix laser</task>'
                    f'  </planned>'
                    f'  <completed/>'
                    f'</maintenance>')
    xml.raises(r'not a valid value of the atomic type')


@pytest.mark.parametrize('date', ['2023-05-24', '2100-01-01'])
def test_planned_task_valid_date_due(xml, date):
    xml.maintenance(f'<maintenance>'
                    f'  <planned>'
                    f'    <task dateDue="{date}">Fix laser</task>'
                    f'  </planned>'
                    f'  <completed/>'
                    f'</maintenance>')
    assert xml.is_valid()


@pytest.mark.parametrize(
    'attribs',
    [{'dateDue': '2024-10-10'},
     {'dateDue': '2024-10-10', 'performedBy': ''},
     {'performedBy': 'Light, MSL', 'dateDue': '2024-10-10'}]
)
def test_planned_task_valid_attributes(xml, attribs):
    task = xml.element('task', text='Fixme', **attribs)
    xml.maintenance(f'<maintenance>'
                    f'  <planned>'
                    f'    {task}'
                    f'  </planned>'
                    f'  <completed/>'
                    f'</maintenance>')
    assert xml.is_valid()


@pytest.mark.parametrize(
    'attribs',
    [{'apple': 'red'},
     {'dateDue': '2024-10-10', 'apple': 'red'},
     {'performedBy': 'Light, MSL', 'apple': 'red', 'dateDue': '2024-10-10'}]
)
def test_planned_task_invalid_attribute(xml, attribs):
    task = xml.element('task', text='Fixme', **attribs)
    xml.maintenance(f'<maintenance>'
                    f'  <planned>'
                    f'    {task}'
                    f'  </planned>'
                    f'  <completed/>'
                    f'</maintenance>')
    xml.raises(r"The attribute 'apple' is not allowed")


def test_planned_task_multiple_invalid_name(xml):
    xml.maintenance('<maintenance>'
                    '  <planned>'
                    '    <task dateDue="2024-10-10">Fixme</task>'
                    '    <tasks dateDue="2024-10-10">Fixme</tasks>'
                    '    <task dateDue="2024-10-10">Fixme</task>'
                    '  </planned>'
                    '  <completed/>'
                    '</maintenance>')
    xml.raises(r"tasks': This element is not expected")


def test_planned_task_multiple_invalid_text(xml):
    xml.maintenance('<maintenance>'
                    '  <planned>'
                    '    <task dateDue="2024-10-10">Fixme</task>'
                    '    <task dateDue="2024-10-10"></task>'
                    '    <task dateDue="2024-10-10">Fixme</task>'
                    '  </planned>'
                    '  <completed/>'
                    '</maintenance>')
    xml.raises(r"not accepted by the pattern")


def test_planned_task_multiple_valid(xml):
    xml.maintenance('<maintenance>'
                    '  <planned>'
                    '    <task dateDue="2024-10-10">Fixme</task>'
                    '    <task dateDue="2024-10-10">Fixme</task>'
                    '    <task dateDue="2024-10-10">Fixme</task>'
                    '    <task dateDue="2024-10-10">Fixme</task>'
                    '    <task dateDue="2024-10-10">Fixme</task>'
                    '  </planned>'
                    '  <completed/>'
                    '</maintenance>')
    assert xml.is_valid()


def test_completed_invalid_subelement(xml):
    xml.maintenance('<maintenance>'
                    '  <planned/>'
                    '  <completed>'
                    '    <event>Service laser</event>'
                    '  </completed>'
                    '</maintenance>')
    xml.raises(r"event': This element is not expected")


def test_completed_task_no_attributes(xml):
    xml.maintenance('<maintenance>'
                    '  <planned/>'
                    '  <completed>'
                    '    <task>Service laser</task>'
                    '  </completed>'
                    '</maintenance>')
    xml.raises(r"The attribute 'dateDue' is required but missing")


def test_completed_task_date_completed_missing(xml):
    xml.maintenance('<maintenance>'
                    '  <planned/>'
                    '  <completed>'
                    '    <task dateDue="2024-10-10" performedBy="MSL">Service laser</task>'
                    '  </completed>'
                    '</maintenance>')
    xml.raises(r"The attribute 'dateCompleted' is required but missing")


def test_completed_task_performed_by_missing(xml):
    xml.maintenance('<maintenance>'
                    '  <planned/>'
                    '  <completed>'
                    '    <task dateDue="2024-10-10" dateCompleted="2024-10-10">Service laser</task>'
                    '  </completed>'
                    '</maintenance>')
    xml.raises(r"The attribute 'performedBy' is required but missing")


@pytest.mark.parametrize('text', INVALID_TASK_TEXT)
def test_completed_task_invalid_text(xml, text):
    xml.maintenance(f'<maintenance>'
                    f'  <planned/>'
                    f'  <completed>'
                    f'    <task dateDue="2024-10-10" dateCompleted="2024-10-10" performedBy="MSL">{text}</task>'
                    f'  </completed>'
                    f'</maintenance>')
    xml.raises('not accepted by the pattern')


@pytest.mark.parametrize('date', INVALID_DATES)
def test_completed_task_invalid_date_due(xml, date):
    xml.maintenance(f'<maintenance>'
                    f'  <planned/>'
                    f'  <completed>'
                    f'    <task dateDue="{date}" dateCompleted="2024-10-10" performedBy="MSL">Service laser</task>'
                    f'  </completed>'
                    f'</maintenance>')
    xml.raises(r'not a valid value of the atomic type')


@pytest.mark.parametrize('date', INVALID_DATES)
def test_completed_task_invalid_date_completed(xml, date):
    xml.maintenance(f'<maintenance>'
                    f'  <planned/>'
                    f'  <completed>'
                    f'    <task dateDue="2024-10-10" dateCompleted="{date}" performedBy="MSL">Service laser</task>'
                    f'  </completed>'
                    f'</maintenance>')
    xml.raises(r'not a valid value of the atomic type')


@pytest.mark.parametrize('by', ['', ' ', '    ', '\t\t\t', '  \n', '\r', '\r\n'])
def test_completed_task_invalid_performed_by(xml, by):
    xml.maintenance(f'<maintenance>'
                    f'  <planned/>'
                    f'  <completed>'
                    f'    <task dateDue="2024-10-10" dateCompleted="2024-10-10" performedBy="{by}">Service laser</task>'
                    f'  </completed>'
                    f'</maintenance>')
    xml.raises(r'not accepted by the pattern')


@pytest.mark.parametrize('date', ['2023-05-24', '2100-01-01'])
def test_completed_task_valid_date_due(xml, date):
    xml.maintenance(f'<maintenance>'
                    f'  <planned/>'
                    f'  <completed>'
                    f'    <task dateDue="{date}" dateCompleted="2024-10-10" performedBy="MSL">Service laser</task>'
                    f'  </completed>'
                    f'</maintenance>')
    assert xml.is_valid()


@pytest.mark.parametrize('date', ['2023-05-24', '2100-01-01'])
def test_completed_task_valid_date_completed(xml, date):
    xml.maintenance(f'<maintenance>'
                    f'  <planned/>'
                    f'  <completed>'
                    f'    <task dateDue="2024-10-10" dateCompleted="{date}" performedBy="MSL">Service laser</task>'
                    f'  </completed>'
                    f'</maintenance>')
    assert xml.is_valid()


@pytest.mark.parametrize('by', ['Light', 'Light@MSL', 'An external company X'])
def test_completed_task_valid_performed_by(xml, by):
    xml.maintenance(f'<maintenance>'
                    f'  <planned/>'
                    f'  <completed>'
                    f'    <task dateDue="2024-10-10" dateCompleted="2024-10-10" performedBy="{by}">Service laser</task>'
                    f'  </completed>'
                    f'</maintenance>')
    assert xml.is_valid()


@pytest.mark.parametrize(
    'attribs',
    [{'dateDue': '2024-10-10', 'dateCompleted': '2024-10-10', 'performedBy': 'Me'},
     {'performedBy': 'Me', 'dateDue': '2024-10-10', 'dateCompleted': '2024-10-10'},
     {'dateCompleted': '2024-10-10', 'performedBy': 'Light, MSL', 'dateDue': '2024-10-10'}]
)
def test_completed_task_valid_attributes(xml, attribs):
    task = xml.element('task', text='Fixme', **attribs)
    xml.maintenance(f'<maintenance>'
                    f'  <planned/>'
                    f'  <completed>'
                    f'    {task}'
                    f'  </completed>'
                    f'</maintenance>')
    assert xml.is_valid()


@pytest.mark.parametrize(
    'attribs',
    [{'apple': 'red'},
     {'dateDue': '2024-10-10', 'apple': 'red', 'dateCompleted': '2024-10-10', 'performedBy': 'Me'},
     {'performedBy': 'Me', 'dateDue': '2024-10-10', 'apple': 'red', 'dateCompleted': '2024-10-10'},
     {'dateCompleted': '2024-10-10', 'performedBy': 'Light, MSL', 'apple': 'red', 'dateDue': '2024-10-10'}]
)
def test_completed_task_invalid_attribute(xml, attribs):
    task = xml.element('task', text='Fixme', **attribs)
    xml.maintenance(f'<maintenance>'
                    f'  <planned/>'
                    f'  <completed>'
                    f'    {task}'
                    f'  </completed>'
                    f'</maintenance>')
    xml.raises(r"The attribute 'apple' is not allowed")


def test_completed_task_multiple_invalid_name(xml):
    xml.maintenance('<maintenance>'
                    '  <planned/>'
                    '  <completed>'
                    '    <task dateDue="2024-10-10" dateCompleted="2024-10-10" performedBy="MSL">Fixme</task>'
                    '    <tasks dateDue="2024-10-10" dateCompleted="2024-10-10" performedBy="MSL">Fixme</tasks>'
                    '    <task dateDue="2024-10-10" dateCompleted="2024-10-10" performedBy="MSL">Fixme</task>'
                    '  </completed>'
                    '</maintenance>')
    xml.raises(r"tasks': This element is not expected")


def test_completed_task_multiple_invalid_text(xml):
    xml.maintenance('<maintenance>'
                    '  <planned/>'
                    '  <completed>'
                    '    <task dateDue="2024-10-10" dateCompleted="2024-10-10" performedBy="MSL">Fixme</task>'
                    '    <task dateDue="2024-10-10" dateCompleted="2024-10-10" performedBy="MSL"></task>'
                    '    <task dateDue="2024-10-10" dateCompleted="2024-10-10" performedBy="MSL">Fixme</task>'
                    '  </completed>'
                    '</maintenance>')
    xml.raises(r"not accepted by the pattern")


def test_completed_task_multiple_valid(xml):
    xml.maintenance('<maintenance>'
                    '  <planned/>'
                    '  <completed>'
                    '    <task dateDue="2024-10-10" dateCompleted="2024-10-10" performedBy="MSL">Fixme</task>'
                    '    <task dateDue="2024-10-10" dateCompleted="2024-10-10" performedBy="MSL">Fixme</task>'
                    '    <task dateDue="2024-10-10" dateCompleted="2024-10-10" performedBy="MSL">Fixme</task>'
                    '    <task dateDue="2024-10-10" dateCompleted="2024-10-10" performedBy="MSL">Fixme</task>'
                    '    <task dateDue="2024-10-10" dateCompleted="2024-10-10" performedBy="MSL">Fixme</task>'
                    '  </completed>'
                    '</maintenance>')
    assert xml.is_valid()


def test_planned_and_completed_task_multiple(xml):
    xml.maintenance('<maintenance>'
                    '  <planned>'
                    '    <task dateDue="2024-10-10">Fixme</task>'
                    '    <task dateDue="2024-10-10">Fixme</task>'
                    '  </planned>'
                    '  <completed>'
                    '    <task dateDue="2024-10-10" dateCompleted="2024-10-10" performedBy="MSL">Fixme</task>'
                    '    <task dateDue="2024-10-10" dateCompleted="2024-10-10" performedBy="MSL">Fixme</task>'
                    '    <task dateDue="2024-10-10" dateCompleted="2024-10-10" performedBy="MSL">Fixme</task>'
                    '  </completed>'
                    '</maintenance>')
    assert xml.is_valid()
