# /// script
# requires-python = ">=3.9"
# dependencies = [
#   "lxml",
#   "GTC",
# ]
# ///
from __future__ import annotations

import logging
from hashlib import sha256
from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np
from GTC.persistence import loads_json
from GTC.xml_format import xml_to_archive
from lxml import etree

if TYPE_CHECKING:
    from typing import TextIO, BinaryIO
    from lxml.etree import Element, ElementTree, XMLSchema

__all__ = ('load_schema', 'recursive_validate', 'validate')


def load_schema(path: str | Path = 'equipment-register.xsd') -> None:
    """Load the Equipment-Register Schema file.

    :param path: The path to the Schema file.
    """
    global schema
    schema = etree.XMLSchema(etree.parse(path))


def recursive_validate(
        start_dir: str | Path,
        *,
        pattern: str = '*.xml',
        root_dir: str | Path = '',
        **variables) -> int:
    """Recursively find and validate all equipment-register files.

    :param start_dir: The starting directory to recursively find and validate
        all equipment-register files.

    :param pattern: The glob pattern to use to find equipment-register files.

    :param root_dir: The root directory to use when a calibration report is
        located in an external file. The `root_dir` value, i.e.,
        `root_dir \\ <directory> \\ <filename>`, may be required to build
        the absolute path to the file. The `<directory>` and `<filename>`
        values are child elements of the `<file>` element.

    :param variables: A mapping between a variable name and its value
        if the calibration report is in the form of an equation. By default,
        the variable name is determined automatically from the `<value>`
        and `<uncertainty>` attributes and a value of 1.0 is assigned to
        all variables.

    :return: The number of files that were validated.
    """
    n = 0
    for path in Path(start_dir).rglob(pattern):
        tree = etree.parse(path)
        if tree.getroot().tag == f'{{{namespace}}}register':
            logger.debug('Processing %s', path)
            validate(tree, root_dir=root_dir, **variables)
            n += 1
    return n


def validate(register: str | Path | TextIO | BinaryIO | ElementTree,
             *,
             root_dir: str | Path = '',
             **variables) -> None:
    """Validate an equipment register.

    :param register: The path to a file, a file-like object
        or an ElementTree that is an equipment register.

    :param root_dir: The root directory to use when a calibration report is
        located in an external file. The `root_dir` value, i.e.,
        `root_dir \\ <directory> \\ <filename>`, may be required to build
        the absolute path to the file. The `<directory>` and `<filename>`
        values are child elements of the `<file>` element.

    :param variables: A mapping between a variable name and its value
        if the calibration report is in the form of an equation. By default,
        the variable name is determined automatically from the `<value>`
        and `<uncertainty>` attributes and a value of 1.0 is assigned to
        all variables.
    """
    if schema is None:
        load_schema()

    tree: ElementTree
    if hasattr(register, 'xpath'):
        tree = register
    else:
        logger.debug('Processing %s', register)
        tree = etree.parse(register)
    schema.assertValid(tree)

    nsmap = {'reg': namespace}
    for equipment in tree.xpath('//reg:equipment', namespaces=nsmap):
        manufacturer, model, serial = equipment[1:4]  # schema forces order
        name = f'{manufacturer.text} {model.text} {serial.text}'
        for equation in equipment.xpath('.//reg:equation', namespaces=nsmap):
            _equation(equation, debug_name=name, nsmap=nsmap, **variables)
        for file in equipment.xpath('.//reg:file', namespaces=nsmap):
            _file(file, root=root_dir, debug_name=name)
        for serialised in equipment.xpath('.//reg:serialised', namespaces=nsmap):
            _serialised(serialised, debug_name=name)
        for table in equipment.xpath('.//reg:table', namespaces=nsmap):
            _table(table, debug_name=name)


def _equation(equation: Element, *, debug_name: str, nsmap: dict[str, str], **variables) -> None:
    """Validates that the equations are valid."""
    logger.debug('  [%s] Validating equations for %s ', debug_name)

    value, uncertainty = equation[:2]  # schema forces order

    names = value.attrib['variables'].split()
    names += uncertainty.attrib['variables'].split()
    names = set(names)
    loc = {n: 1.0 for n in names}
    loc.update(eqn_map)
    loc.update(variables)

    range_names = equation.xpath(".//reg:range/@variable", namespaces=nsmap)
    range_name_set = set(range_names)
    if len(range_names) != len(range_name_set):
        raise AssertionError(
            f'The names of the range variables are not unique for {debug_name!r}\n'
            f'variable names: {", ".join(sorted(range_names))}'
        )

    if len(names) != len(range_names) or names.difference(range_name_set):
        raise AssertionError(
            f'The equation variables and the range variables are not the same for {debug_name!r}\n'
            f'equation variables: {", ".join(sorted(names))}\n'
            f'range variables   : {", ".join(sorted(range_names))}'
        )

    try:
        eval(value.text, {'__builtins__': {}}, loc)
        eval(uncertainty.text, {'__builtins__': {}}, loc)
    except Exception as e:
        raise AssertionError(
            f'Invalid equation syntax for {debug_name!r}\n'
            f'{e.__class__.__name__}: {e}'
        ) from e


def _file(file: Element, *, root: str | Path, debug_name: str) -> None:
    """Validates that the file exists and that the SHA-256 checksum is correct."""
    directory, filename, checksum = file[:3]  # schema forces order

    path = Path(root)
    if directory.text:
        path /= directory.text
    path /= filename.text

    logger.debug('  [%s] Validating SHA-256 checksum for %s ', debug_name, path)

    sha = sha256()
    with open(path, mode='rb') as f:
        while True:
            data = f.read(65536)
            if not data:
                break
            sha.update(data)

    specified = checksum.text.lower()
    expected = sha.hexdigest()
    if expected != specified:
        raise AssertionError(
            f'The SHA-256 checksum for {path} does not match\n'
            f'expected={expected}\n'
            f'<sha256>={specified}'
        )


def _serialised(serialised: Element, *, debug_name: str) -> None:
    """Validates that the serialised content is a valid GTC Archive.

    Other serialisation formats are silently ignored.
    """
    fmt = serialised[0]
    try:
        if fmt.tag.endswith('gtcArchive'):
            logger.debug('  [%s] Validating gtcArchive', debug_name)
            xml_to_archive(fmt)
        elif fmt.tag.endswith('gtcArchiveJSON'):
            logger.debug('  [%s] Validating gtcArchiveJSON', debug_name)
            loads_json(fmt.text)
    except Exception as e:
        raise AssertionError(
            f'Invalid serialised GTC Archive for {debug_name!r}\n'
            f'{e.__class__.__name__}: {e}'
        ) from e


def _table(table: Element, *, debug_name: str) -> None:
    """Validates that the data types, header and data are valid."""
    logger.debug('  [%s] Validating table', debug_name)

    types, unit, header, data = table[:4]  # schema forces order
    types = [t.strip() for t in types.text.split(',')]
    units = [u.strip() for u in unit.text.split(',')]
    header = [h.strip() for h in header.text.split(',')]

    if len(types) != len(units):
        raise AssertionError(
            f'The table "type" and "unit" have different lengths for {debug_name!r}\n'
            f'type={types}\n'
            f'unit={units}'
        )

    if len(types) != len(header):
        raise AssertionError(
            f'The table "type" and "header" have different lengths for {debug_name!r}\n'
            f'type={types}\n'
            f'header={header}'
        )

    len_types = len(types)
    for row_line in data.text.split('\n'):
        row_stripped = row_line.strip()
        if not row_stripped:
            continue
        row = list(col.strip() for col in row_stripped.split(','))
        if len_types != len(row):
            raise AssertionError(
                f'The table "data" does not have the expected number of columns for {debug_name!r}\n'
                f'Expected {len_types} columns, row data is {row_stripped!r}'
            )
        for typ, col in zip(types, row):
            try:
                dtype_value_check[typ](col)
            except Exception as e:
                raise AssertionError(
                    f'Invalid table data for {debug_name!r}\n'
                    f'{e.__class__.__name__}: {e}'
                ) from e


def _bool(value: str) -> None:
    """A bool in the table data must only be allowed to have certain values."""
    if value not in booleans:
        expected = ', '.join(booleans)
        raise ValueError(
            f'Invalid bool value {value}, must be one of: {expected}'
        )


def _int32(value: str) -> None:
    """An int in the table data must be in the int32 range."""
    int32 = int(value)
    if int32 < -2147483648 or int32 > 2147483647:
        raise ValueError(
            f'Invalid int value {value}, must be in range [-2147483648, 2147483647]'
        )


def _double(value: str) -> None:
    """A double in the table data must be able to be converted to a float."""
    float(value)


def _string(value: str) -> None:
    """No-op. A string in the table data is already a string."""
    str(value)


logger = logging.getLogger('register')

schema: XMLSchema | None = None

booleans = ('true', 'True', 'TRUE', '1', 'false', 'False', 'FALSE', '0')

namespace = 'https://measurement.govt.nz/equipment-register'

dtype_value_check = {
    'bool': _bool,
    'int': _int32,
    'double': _double,
    'string': _string,
}

eqn_map = {
    'pi': np.pi,
    'pow': np.pow,
    'sqrt': np.sqrt,
    'sin': np.sin,
    'asin': np.asin,
    'cos': np.cos,
    'acos': np.acos,
    'tan': np.tan,
    'atan': np.atan,
    'exp': np.exp,
    'ln': np.log,
    'log': np.log10,
}
