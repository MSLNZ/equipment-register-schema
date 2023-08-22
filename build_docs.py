"""
Create the ``docs/index.html`` and ``docs/diagram.svg`` files.
"""
import os
import sys
from subprocess import run

from lxml import etree, __version__

os.chdir('docs')

# write to stderr instead of stdout because stderr is where the
# Java log messages are written to
print(f'lxml version {__version__}', file=sys.stderr)

# Check that java is available
try:
    run(['java', '-version'])
except FileNotFoundError:
    sys.exit('You need java installed and available on PATH')

# Build SVG file
run(['java', '-jar', 'bin/xsdvi.jar',
     '../equipment-register.xsd',
     '-useStyle', 'styles/svg.css'])
os.replace('equipment-register.svg', 'diagram.svg')

# Build HTML file
xsd = etree.parse('../equipment-register.xsd')
xsl = etree.parse('styles/xs3p-msl.xsl')
transform = etree.XSLT(xsl)
result = transform(xsd)
result.write_output('index.html')
