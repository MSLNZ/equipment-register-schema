# /// script
# requires-python = ">=3.9"
# dependencies = [
#   "lxml",
#   "GTC",
# ]
# ///
#
# You can use PyInstaller to build into a portable executable
# ..\tools> py -m PyInstaller validate.py --add-data ..\equipment-register.xsd:..
from __future__ import annotations

import logging
import re
import sys
from hashlib import sha256
from pathlib import Path
from typing import TYPE_CHECKING
from urllib.parse import urlparse

import numpy as np
from GTC.persistence import loads_json
from GTC.xml_format import xml_to_archive
from lxml import etree

if TYPE_CHECKING:
    from typing import TextIO, BinaryIO
    from lxml.etree import Element, ElementTree, XMLSchema

__all__ = ('load_schema', 'next_id', 'recursive_validate', 'validate')

ID_PATTERN = r'(?P<digits>\d+)'


def next_id(
        dir_or_file: str | Path,
        *,
        id_pattern: str = ID_PATTERN,
        file_pattern: str = '*.xml',
        flags: int = 0) -> int:
    r"""Recursively search all equipment-register files in a directory or within a
    single file to determine the numerical value for the next equipment ID.

    :param dir_or_file: The starting directory to recursively find all
        equipment-register files or a specific file.

    :param id_pattern: A regex (regular expression) pattern to filter equipment IDs.
        For example, if the format of the equipment ID that you are interested in
        is ``MSLE.O.CR####``, you could set `pattern` to be ``r'CR(?P<digits>\d+)'``
        to only consider ID's that have ``CR`` before the numeric part. The `pattern`
        must contain a `digits` named capture group, ``(?P<digits>\d+)``,
        that only contains the digits 0-9.

    :param file_pattern: A glob pattern to use to help filter equipment-register files.

    :param flags: Regex flags to pass to :func:`re.compile`.

    :return: The numeric value for the next equipment ID that is available
        (increments the captured `digits` value by 1). If no equipment IDs
        were found, the returned value is 0.
    """
    def process_file(file, digits) -> int:
        tree = etree.parse(file)
        if tree.getroot().tag != f'{{{namespace}}}register':
            return digits

        logger.debug('Processing %s', file)
        for text in tree.xpath('./reg:equipment/reg:id/text()', namespaces=nsmap):
            match = regex.search(text)
            if match is not None:
                logger.debug('  Found match %r', text)
                digits = max(digits, int(match['digits']))
        return digits

    latest = -1
    nsmap = {'reg': namespace}
    regex = re.compile(id_pattern, flags=flags)

    df = Path(dir_or_file)
    if df.is_file():
        latest = process_file(df, latest)
    else:
        for path in df.rglob(file_pattern):
            latest = process_file(path, latest)

    return latest + 1


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

    :param pattern: The glob pattern to use to help filter equipment-register files.

    :param root_dir: The root directory to use when a calibration report is
        located in an external file. The `root_dir` value, i.e.,
        `root_dir \\ <url>`, may be required to build the absolute path to
        the file. The `<url>` element is a child of a `<file>` or a
        `<digitalReport>` element.

    :param variables: A mapping between a variable name and its value
        if the calibration report is in the form of an equation. By default,
        the variable name is determined automatically from the `<value>`
        and `<uncertainty>` attributes and a value of 1.0 is assigned to
        all variables.

    :return: The number of files that were validated.
    """
    n = 0
    all_ids: set[str] = set()
    for path in Path(start_dir).rglob(pattern):
        logger.debug('Processing %s', path)
        try:
            tree = etree.parse(path)
        except etree.XMLSyntaxError as e:
            logger.debug('  XMLSyntaxWarning! %s', e)
            continue

        tag = tree.getroot().tag
        if tag != f'{{{namespace}}}register':
            logger.debug('  XMLNamespaceWarning! Not a valid equipment-register namespace %r', tag)
            continue

        ids = validate(tree, root_dir=root_dir, **variables)
        for id_ in ids:
            if id_ in all_ids:
                raise AssertionError(f'Duplicate equipment ID ({id_}) found in {path}')
        all_ids.update(ids)
        n += 1

    return n


def validate(register: str | Path | TextIO | BinaryIO | ElementTree,
             *,
             root_dir: str | Path = '',
             **variables) -> set[str]:
    """Validate an equipment register.

    :param register: The path to a file, a file-like object
        or an ElementTree that is an equipment register.

    :param root_dir: The root directory to use when a calibration report is
        located in an external file. The `root_dir` value, i.e.,
        `root_dir \\ <url>`, may be required to build the absolute path to
        the file. The `<url>` element is a child of a `<file>` or a
        `<digitalReport>` element.

    :param variables: A mapping between a variable name and its value
        if the calibration report is in the form of an equation. By default,
        the variable name is determined automatically from the `<value>`
        and `<uncertainty>` attributes and a value of 1.0 is assigned to
        all variables.

    :return: A set of equipment ID's.
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
    ids: set[str] = set()  # schema forces uniqueness within a single XML file
    for equipment in tree.xpath('//reg:equipment', namespaces=nsmap):
        id_, manufacturer, model, serial = equipment[:4]  # schema forces order
        ids.add(id_.text)
        name = f'{manufacturer.text} {model.text} {serial.text}'
        for digital_report in equipment.xpath('.//reg:digitalReport', namespaces=nsmap):
            _file(digital_report, root=root_dir, debug_name=name)
        for equation in equipment.xpath('.//reg:equation', namespaces=nsmap):
            _equation(equation, debug_name=name, nsmap=nsmap, **variables)
        for file in equipment.xpath('.//reg:file', namespaces=nsmap):
            _file(file, root=root_dir, debug_name=name)
        for serialised in equipment.xpath('.//reg:serialised', namespaces=nsmap):
            _serialised(serialised, debug_name=name)
        for table in equipment.xpath('.//reg:table', namespaces=nsmap):
            _table(table, debug_name=name)
    return ids


def _equation(equation: Element, *, debug_name: str, nsmap: dict[str, str], **variables) -> None:
    """Validates that the equations are valid."""
    logger.debug('  [%s] Validating equation element', debug_name)

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
    url, checksum = file[:3]  # schema forces order
    u = urlparse(url.text)

    # check len() > 1 to ignore a Windows drive letter being interpreted as a scheme
    if len(u.scheme) > 1 and u.scheme != 'file':
        raise ValueError(
            f'The url scheme {u.scheme!r} is not yet implemented for {debug_name!r}\n'
            f'url={url.text}'
        )

    path = Path(root)

    if u.netloc:
        if ':' in u.netloc:
            path /= u.netloc
        else:
            path /= f'//{u.netloc}'

    if sys.platform == 'win32':
        path /= u.path.lstrip('/')
    else:
        path /= u.path

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
            f'The SHA-256 checksum of {path} does not match for {debug_name!r}\n'
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
    'log': np.log,
    'log10': np.log10,
}


def cli(*args):
    """Command line interface to validate equipment registers.

    :param args: Command-line arguments.
    """
    import argparse

    parser = argparse.ArgumentParser(
        description='Validate Equipment Registers.',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        'register',
        help='an equipment-register file or a directory containing equipment-register files'
    )
    parser.add_argument(
        '-s', '--schema',
        default=r'.\equipment-register.xsd',
        help='path to the equipment-register schema file [default: ".\\equipment-register.xsd"]'
    )
    parser.add_argument(
        '-p', '--pattern',
        default='*.xml',
        help='glob pattern to use to help filter equipment-register files [default: "*.xml"]'
    )
    parser.add_argument(
        '-r', '--root-dir',
        default='',
        help='root directory to use when a calibration report is located in an external file [default: ""]'
    )
    parser.add_argument(
        '-i', '--id-pattern',
        default=ID_PATTERN,
        help=f'regex pattern to filter equipment IDs [default: {ID_PATTERN}]\n'
             f'(only used if --next-id is specified)'
    )
    parser.add_argument(
        '-n', '--next-id',
        action='store_true',
        help='whether to show the next equipment ID, rather than validating the register'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='whether to show DEBUG logging messages'
    )
    parser.add_argument(
        '-V', '--version',
        action='version',
        version='0.1.0',
        help='show version number and exit'
    )

    if not args:
        args = ['--help']
    args = parser.parse_args(args)

    if args.verbose:
        import logging
        logging.basicConfig(level=logging.DEBUG, format='%(message)s')

    p = Path(args.register)
    if not p.exists():
        print(f'Error! Cannot find "{p}"')
    elif args.next_id:
        print(next_id(p, id_pattern=args.id_pattern, file_pattern=args.pattern))
    elif p.is_dir():
        recursive_validate(p, pattern=args.pattern, root_dir=args.root_dir)
    else:
        validate(p, root_dir=args.root_dir)


if __name__ == '__main__':
    sys.exit(cli(*sys.argv[1:]))
