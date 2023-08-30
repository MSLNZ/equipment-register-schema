"""
Configure pytest.
"""
from __future__ import annotations

import pytest
from lxml import etree
from lxml.etree import DocumentInvalid

schema = etree.XMLSchema(etree.parse('equipment-register.xsd'))


class XML:

    DECLARATION: str = '<?xml version="1.0"?>'
    NAMESPACE: str = 'https://www.measurement.govt.nz/equipment-register'

    def __init__(self) -> None:
        super().__init__()
        self.source: str = ''
        self._root_prefix: str = f'<register team="Light" xmlns="{XML.NAMESPACE}">'
        self._root_suffix: str = '</register>'
        self._equipment_prefix: str = f'<equipment category="DigitalMultiMeter">'
        self._equipment_suffix: str = '</equipment>'
        self._id: str = self.element('id', text='MSLE.L.000')
        self._manufacturer: str = self.element('manufacturer', text='Company, Inc.')
        self._model: str = self.element('model', text='XY-12.3')
        self._serial: str = self.element('serial', text='0123A')
        self._description: str = self.element('description', text='Digital multimeter')
        self._location: str = self.element('location', text='General')
        self._status: str = self.element('status', text='Active')
        self._calibratable: str = self.element('calibratable', text='false')
        self._calibrations: str = self.element('calibrations')
        self._documentation: str = self.element('documentation')
        self._firmware: str = self.element('firmware')
        self._maintenance: str = self.element('maintenance')
        self._custom: str = ''

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
        if self._calibratable:
            elements.append(f'    {self._calibratable}')
        if self._calibrations:
            elements.append(f'    {self._calibrations}')
        if self._documentation:
            elements.append(f'    {self._documentation}')
        if self._firmware:
            elements.append(f'    {self._firmware}')
        if self._maintenance:
            elements.append(f'    {self._maintenance}')
        if self._custom:
            elements.append(f'    {self._custom}')
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

    def calibratable(self, obj: str | int, **attribs) -> None:
        self._calibratable = self._helper(self._calibratable, 'calibratable', obj, **attribs)

    def custom(self, string: str) -> None:
        self._custom = string

    def maintenance(self, string: str) -> None:
        self._maintenance = string


@pytest.fixture(scope='function')
def xml() -> XML:
    return XML()
