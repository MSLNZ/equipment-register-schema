import pytest

from tests.conftest import INVALID_DATES

def test_invalid_name(xml):
    xml.alterations('<invalid/>')
    xml.raises(r'Expected is .*alterations')


def test_empty(xml):
    xml.alterations('<alterations/>')
    assert xml.is_valid()


def test_repeated(xml):
    xml.alterations('<alterations/><alterations/>')
    xml.raises(r'Expected is .*firmware')


def test_no_top_level_attribute_allowed(xml):
    xml.alterations('<alterations dateDue="2024-10-10"/>')
    xml.raises(r"alterations', attribute 'dateDue'")


def test_unexpected_child(xml):
    xml.alterations('<alterations><task/></alterations>')
    xml.raises(r"task': This element is not expected")


def test_date_missing(xml):
    xml.alterations('<alterations>'
                    '  <alteration>Repair</alteration>'
                    '</alterations>')
    xml.raises(r"attribute 'date' is required but missing")


@pytest.mark.parametrize('date', INVALID_DATES)
def test_invalid_date(xml, date):
    xml.alterations(f'<alterations>'
                    f'  <alteration date="{date}" performedBy="MSL">Repair</alteration>'
                    f'</alterations>')
    xml.raises(r'not a valid value of the atomic type')


@pytest.mark.parametrize('date', ['2023-05-24', '2100-01-01'])
def test_valid_date(xml, date):
    xml.alterations(f'<alterations>'
                    f'  <alteration date="{date}" performedBy="MSL">Repair</alteration>'
                    f'</alterations>')
    assert xml.is_valid()


def test_performed_by_missing(xml):
    xml.alterations('<alterations>'
                    '  <alteration date="2024-10-10">Repair</alteration>'
                    '</alterations>')
    xml.raises(r"attribute 'performedBy' is required but missing")


@pytest.mark.parametrize('by', ['', ' ', '    ', '\t\t\t', '  \n', '\r', '\r\n'])
def test_performed_by_invalid(xml, by):
    xml.alterations(f'<alterations>'
                    f'  <alteration date="2024-10-10" performedBy="{by}">Repair</alteration>'
                    f'</alterations>')
    xml.raises(r'not accepted by the pattern')


@pytest.mark.parametrize('by', ['Light', 'Light@MSL', 'An external company X'])
def test_performed_by_valid(xml, by):
    xml.alterations(f'<alterations>'
                    f'  <alteration date="2024-10-10" performedBy="{by}">Repair</alteration>'
                    f'</alterations>')
    assert xml.is_valid()


@pytest.mark.parametrize(
    'attribs',
    [{'apple': 'red'},
     {'date': '2024-10-10', 'apple': 'red'},
     {'performedBy': 'Light, MSL', 'apple': 'red', 'date': '2024-10-10'}]
)
def test_invalid_attributes(xml, attribs):
    alteration = xml.element('alteration', text='Repair', **attribs)
    xml.alterations(f'<alterations>'
                    f'  {alteration}'
                    f'</alterations>')
    xml.raises(r"The attribute 'apple' is not allowed")


def test_multiple_invalid_child(xml):
    xml.alterations('<alterations>'
                    '  <alteration date="2024-10-10" performedBy="MSL">Repair</alteration>'
                    '  <action date="2024-10-10" performedBy="MSL">Repair</action>'
                    '</alterations>')
    xml.raises(r"action': This element is not expected")


def test_multiple_valid(xml):
    xml.alterations('<alterations>'
                    '  <alteration date="2024-10-10" performedBy="MSL">Repair</alteration>'
                    '  <alteration date="2024-10-10" performedBy="MSL">Repair</alteration>'
                    '  <alteration date="2024-10-10" performedBy="MSL">Repair</alteration>'
                    '  <alteration date="2024-10-10" performedBy="MSL">Repair</alteration>'
                    '</alterations>')
    assert xml.is_valid()


def test_multiple_invalid_text(xml):
    xml.alterations('<alterations>'
                    '  <alteration date="2024-10-10" performedBy="MSL">Repair</alteration>'
                    '  <alteration date="2024-10-10" performedBy="MSL">Repair</alteration>'
                    '  <alteration date="2024-10-10" performedBy="MSL"></alteration>'
                    '</alterations>')
    xml.raises(r"not accepted by the pattern")


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
def test_invalid_text(xml, text):
    xml.alterations(f'<alterations>'
                    f'  <alteration date="2024-10-10" performedBy="MSL">{text}</alteration>'
                    f'</alterations>')
    xml.raises('not accepted by the pattern')


@pytest.mark.parametrize(
    'text',
    ['a',
     ' a',
     'a ',
     '  a     ',
     'Replace the diode',
     ' Replace the    diode',
     'Replace\tthe\tdiode',
     'The diode (model: xxx) is flaky and it should be replaced with a newer model (yyy)',
])
def test_valid_text(xml, text):
    xml.alterations(f'<alterations>'
                    f'  <alteration date="2024-10-10" performedBy="MSL">{text}</alteration>'
                    f'</alterations>')
    assert xml.is_valid()
