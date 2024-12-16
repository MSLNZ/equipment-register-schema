"""
Configure pytest.
"""
from __future__ import annotations
from pathlib import Path

import pytest
from lxml import etree
from lxml.etree import DocumentInvalid

schema = etree.XMLSchema(etree.parse('equipment-register.xsd'))

INVALID_DATES = [
    '',
    '   ',
    '2023',
    '2023-05',
    '2023-13-05',
    '2023-08-32',
    '01-02-03',
    '05-08-2023',
    '08-05-2023',
    'January',
    '24 May 2023',
    'May, 24 2023',
    '2023.03.04',
    '2023 03 04',
    '20230304',
]


class XML:

    FORMAT: str = 'MSL PDF/A-3'
    DECLARATION: str = '<?xml version="1.0"?>'
    NAMESPACE: str = 'https://measurement.govt.nz/equipment-register'
    SHA256: str = '8392e473a047543773138653b98037956fa2086e4a54fc882d913f10cc217728'

    def __init__(self) -> None:
        super().__init__()
        self.source: str = ''
        self._root_prefix: str = f'<register team="Light" xmlns="{XML.NAMESPACE}">'
        self._root_suffix: str = '</register>'
        self._equipment_prefix: str = '<equipment keywords="Laser">'
        self._equipment_suffix: str = '</equipment>'
        self._id: str = self.element('id', text='MSLE.L.000')
        self._manufacturer: str = self.element('manufacturer', text='Company, Inc.')
        self._model: str = self.element('model', text='XY-12.3')
        self._serial: str = self.element('serial', text='0123A')
        self._description: str = self.element('description', text='Digital multimeter')
        self._location: str = self.element('location', text='Kibble Balance')
        self._status: str = self.element('status', text='Active')
        self._loggable: str = self.element('loggable', text='false')
        self._traceable: str = self.element('traceable', text='false')
        self._calibrations: str = self.element('calibrations')
        self._maintenance: str = self.element('maintenance')
        self._alterations: str = self.element('alterations')
        self._firmware: str = self.element('firmware')
        self._specified_requirements: str = self.element('specifiedRequirements')
        self._financial: str = self.element('financial')
        self._documentation: str = self.element('documentation')
        self._extra: str = ''

    def __call__(self):
        return XML()

    def __repr__(self) -> str:
        if self.source:
            return f'{XML.DECLARATION}\n{self.source}'

        elements = [XML.DECLARATION,
                    f'{self._root_prefix}',
                    f'  {self._equipment_prefix}']

        if self._id:
            elements.append(f'    {self._id}')
        if self._manufacturer:
            elements.append(f'    {self._manufacturer}')
        if self._model:
            elements.append(f'    {self._model}')
        if self._serial:
            elements.append(f'    {self._serial}')
        if self._description:
            elements.append(f'    {self._description}')
        if self._location:
            elements.append(f'    {self._location}')
        if self._status:
            elements.append(f'    {self._status}')
        if self._loggable:
            elements.append(f'    {self._loggable}')
        if self._traceable:
            elements.append(f'    {self._traceable}')
        if self._calibrations:
            elements.append(f'    {self._calibrations}')
        if self._maintenance:
            elements.append(f'    {self._maintenance}')
        if self._alterations:
            elements.append(f'    {self._alterations}')
        if self._firmware:
            elements.append(f'    {self._firmware}')
        if self._specified_requirements:
            elements.append(f'    {self._specified_requirements}')
        if self._financial:
            elements.append(f'    {self._financial}')
        if self._documentation:
            elements.append(f'    {self._documentation}')
        if self._extra:
            elements.append(f'    {self._extra}')
        elements.append(f'  {self._equipment_suffix}')
        elements.append(f'{self._root_suffix}')
        return '\n'.join(elements)

    @staticmethod
    def attributes(**kwargs) -> str:
        """Convert the keyword arguments to a string of XML element attributes."""
        return ' '.join(f'{k}="{v}"' for k, v in kwargs.items())

    @staticmethod
    def _helper(element: str, name: str, obj: str | int, **attribs) -> str:
        if isinstance(obj, int):
            return '\n    '.join(element for _ in range(obj))
        return XML.element(name, text=obj, **attribs)

    def is_valid(self) -> bool:
        """Checks whether the XML document is valid."""
        source: str = etree.fromstring(str(self))
        return schema.validate(source)

    def raises(self, match: str) -> None:
        """Checks the DocumentInvalid exception message for matching text."""
        with pytest.raises(DocumentInvalid, match=match):
            self.validate()

    def validate(self) -> None:
        """Asserts that the XML document is valid."""
        source: str = etree.fromstring(str(self))
        schema.assertValid(source)

    @staticmethod
    def element(name: str, *, text: str = None, **attribs) -> str:
        """Create a string representation of a new element."""
        attributes = XML.attributes(**attribs)
        if text:
            if attributes:
                return f'<{name} {attributes}>{text}</{name}>'
            return f'<{name}>{text}</{name}>'

        if attributes:
            return f'<{name} {attributes}/>'
        return f'<{name}/>'

    def root(self, *, name: str = None, namespace: str = None, **attribs) -> None:
        """Overwrite the root element prefix and suffix."""
        if name is None:
            name = 'register'
        if namespace is None:
            namespace = XML.NAMESPACE
        attributes = XML.attributes(**attribs)
        self._root_suffix = f'</{name}>'
        if attributes and namespace:
            self._root_prefix = f'<{name} {attributes} xmlns="{namespace}">'
        elif not attributes and namespace:
            self._root_prefix = f'<{name} xmlns="{namespace}">'
        elif attributes and not namespace:
            self._root_prefix = f'<{name} {attributes}>'
        else:
            self._root_prefix = f'<{name}>'

    def equipment(self, name: str, **attribs) -> None:
        """Overwrite the equipment element prefix and suffix."""
        attributes = XML.attributes(**attribs)
        self._equipment_suffix = f'</{name}>'
        if attributes:
            self._equipment_prefix = f'<{name} {attributes}>'
        else:
            self._equipment_prefix = f'<{name}>'

    def id(self, obj: str | int, **attribs) -> None:
        self._id = self._helper(self._id, 'id', obj, **attribs)

    def manufacturer(self, obj: str | int, **attribs) -> None:
        self._manufacturer = self._helper(self._manufacturer, 'manufacturer', obj, **attribs)

    def model(self, obj: str | int, **attribs) -> None:
        self._model = self._helper(self._model, 'model', obj, **attribs)

    def serial(self, obj: str | int, **attribs) -> None:
        self._serial = self._helper(self._serial, 'serial', obj, **attribs)

    def description(self, obj: str | int, **attribs) -> None:
        self._description = self._helper(self._description, 'description', obj, **attribs)

    def location(self, obj: str | int, **attribs) -> None:
        self._location = self._helper(self._location, 'location', obj, **attribs)

    def status(self, obj: str | int, **attribs) -> None:
        self._status = self._helper(self._status, 'status', obj, **attribs)

    def loggable(self, obj: str | int, **attribs) -> None:
        self._loggable = self._helper(self._loggable, 'loggable', obj, **attribs)

    def traceable(self, obj: str | int, **attribs) -> None:
        self._traceable = self._helper(self._traceable, 'traceable', obj, **attribs)

    def extra(self, string: str) -> None:
        self._extra = string

    def maintenance(self, string: str) -> None:
        self._maintenance = string

    def alterations(self, string: str) -> None:
        self._alterations = string

    def firmware(self, string: str) -> None:
        self._firmware = string

    def specified_requirements(self, string: str) -> None:
        self._specified_requirements = string

    def calibrations(self, obj: str | int, **attribs) -> None:
        cal = self._helper(self._calibrations, 'calibrations', obj, **attribs)
        if cal.endswith('</calibrations>'):
            i = -len('</calibrations>')
            self._calibrations = cal[:i] + '\n    </calibrations>'
        else:
            self._calibrations = cal

    @staticmethod
    def measurand(components: str = '', **attribs) -> str:
        if not attribs:
            attribs = {'quantity': 'Humidity', 'calibrationInterval': '5'}

        attributes = XML.attributes(**attribs)
        measurand = f'<measurand {attributes}'

        if not components:
            return f'\n      {measurand}/>'

        return (f'\n      {measurand}>\n'
                f'  {components}\n'
                f'      </measurand>')

    @staticmethod
    def component(reports: str = '', **attribs) -> str:
        if attribs:
            attributes = XML.attributes(**attribs)
            component = f'<component {attributes}'
        else:
            component = '<component name=""'

        if not reports:
            return f'      {component}/>'

        return (f'      {component}>\n'
                f'          {reports}\n'
                f'        </component>')

    @staticmethod
    def report(*,
               number: str = 'any',
               issue: str = '2023-09-18',
               start: str = '2023-09-18',
               stop: str = '2023-09-18',
               lab: str = 'MSL',
               method: str = '',
               conditions: str = None,
               acceptance_criteria: str = None,
               choice: str = None,
               extra: str = '',
               **attribs) -> str:
        if attribs:
            attributes = XML.attributes(**attribs)
            report = f'<report {attributes}>'
        else:
            report = f'<report id="{number}">'

        if conditions is None:
            conditions = '<conditions/>'

        if acceptance_criteria is None:
            acceptance_criteria = '<acceptanceCriteria/>'

        if choice is None:
            choice = (f'<file>\n'
                      f'              <url>data.dat</url>\n'
                      f'              <sha256>{XML.SHA256}</sha256>\n'
                      f'            </file>')

        if not lab.startswith('<'):
            lab = f'<issuingLaboratory>{lab}</issuingLaboratory>'
        else:
            lab = lab

        return (f'{report}\n'
                f'            <reportIssueDate>{issue}</reportIssueDate>\n'
                f'            <measurementStartDate>{start}</measurementStartDate>\n'
                f'            <measurementStopDate>{stop}</measurementStopDate>\n'
                f'            {lab}\n'
                f'            <technicalProcedure>{method}</technicalProcedure>\n'
                f'            {conditions}\n'
                f'            {acceptance_criteria}\n'                
                f'            {choice}\n'
                f'            {extra}\n'
                f'          </report>')

    @staticmethod
    def digital_report(*, url: str | Path = '', sha256: str = '', number: str = 'any', **attribs) -> str:
        if attribs:
            attributes = XML.attributes(**attribs)
            report = f'<digitalReport {attributes}>'
        else:
            report = f'<digitalReport id="{number}" format="{XML.FORMAT}">'

        if not url:
            url = f'<url>calibration.pdf</url>'
        elif isinstance(url, Path) or (isinstance(url, str) and not url.startswith('<')):
            url = f'<url>{url}</url>'

        if not sha256:
            sha256 = f'<sha256>{XML.SHA256}</sha256>'
        elif not sha256.startswith('<'):
            sha256 = f'<sha256>{sha256}</sha256>'

        return f'{report}{url}{sha256}</digitalReport>'

    @staticmethod
    def table(*,
              datatype: str = 'int',
              unit: str = 'm',
              header: str = 'a',
              data: str = '1') -> str:
        return (f'<table>\n'
                f'              <type>{datatype}</type>\n'
                f'              <unit>{unit}</unit>\n'
                f'              <header>{header}</header>\n'
                f'              <data>{data}</data>\n'
                f'            </table>')

    def financial(self,
                  *,
                  asset_number: str = None,
                  warranty_date: str = None,
                  year_purchased: str = None,
                  **kwargs: dict[str, str]) -> None:
        element = ['<financial>']
        if asset_number is not None:
            element.append(f'<assetNumber>{asset_number}</assetNumber>')
        if warranty_date is not None:
            element.append(f'<warrantyExpirationDate>{warranty_date}</warrantyExpirationDate>')
        if year_purchased is not None:
            element.append(f'<yearPurchased>{year_purchased}</yearPurchased>')
        for k, v in kwargs.items():
            element.append(f'<{k}>{v}</{k}>')
        element.append('</financial>')
        self._financial = ''.join(element)


@pytest.fixture(scope='function')
def xml() -> XML:
    return XML()
