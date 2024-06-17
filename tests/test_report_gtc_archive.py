import pytest


def test_xml_format(xml):
    choice = ('<serialised>'
              '  <gtcArchive version="1.5.0" xmlns="https://measurement.govt.nz/gtc/xml">'
              '    <leafNodes>'
              '      <leafNode uid="(59556220778059068389620836480377249918, 1)">'
              '        <u>1.0</u>'
              '        <df>INF</df>'
              '        <label />'
              '        <independent>true</independent>'
              '      </leafNode>'
              '    </leafNodes>'
              '    <taggedReals>'
              '      <elementaryReal tag="x" uid="(59556220778059068389620836480377249918, 1)">'
              '        <value>1.0</value>'
              '      </elementaryReal>'
              '    </taggedReals>'
              '    <untaggedReals />'
              '    <taggedComplexes />'
              '    <intermediates />'
              '  </gtcArchive>'
              '</serialised>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    assert xml.is_valid()


def test_xml_format_missing_namespace(xml):
    # missing GTC namespace in element
    # <gtcArchive version="1.5.0" xmlns="https://measurement.govt.nz/gtc/xml">
    choice = ('<serialised>'
              '  <gtcArchive version="1.5.0">'
              '    <leafNodes>'
              '      <leafNode uid="(1, 1)">'
              '        <u>1.0</u>'
              '        <df>INF</df>'
              '        <label />'
              '        <independent>true</independent>'
              '      </leafNode>'
              '    </leafNodes>'
              '    <taggedReals>'
              '      <elementaryReal tag="x" uid="(1, 1)">'
              '        <value>1.0</value>'
              '      </elementaryReal>'
              '    </taggedReals>'
              '    <untaggedReals />'
              '    <taggedComplexes />'
              '    <intermediates />'
              '  </gtcArchive>'
              '</serialised>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r"measurement.govt.nz/equipment-register}gtcArchive': This element is not expected.")


def test_xml_format_invalid(xml):
    # The XSD file from GTC determines that this content is invalid
    choice = ('<serialised>'
              '  <gtcArchive version="1.5.0" xmlns="https://measurement.govt.nz/gtc/xml">'
              '    <taggedReals>'
              '      <elementaryReal tag="x" uid="(1, 1)">'
              '        <value>1.0</value>'
              '      </elementaryReal>'
              '    </taggedReals>'
              '    <leafy>'
              '      <value>1.265</value>'
              '      <uncert>0.03</uncert>'
              '      <dof>2.1</dof>'
              '    </leafy>'
              '  </gtcArchive>'
              '</serialised>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r"leafy': This element is not expected.")


def test_json_format(xml):
    choice = ('<serialised>'
              '  <gtcArchiveJSON>{'
              '    "CLASS": "Archive",'
              '    "version": "https://measurement.govt.nz/gtc/json_1.5.0",'
              '    "leaf_nodes": {'
              '      "(118599204086499570505990623620188996074, 1)": {'
              '        "CLASS": "LeafNode",'
              '        "uid": "(118599204086499570505990623620188996074, 1)",'
              '        "label": null,'
              '        "u": 1.0,'
              '        "df": null,'
              '        "independent": true'
              '      }'
              '    },'
              '    "tagged_real": {'
              '      "x": {'
              '        "CLASS": "ElementaryReal",'
              '        "x": 1.0,'
              '        "uid": "(118599204086499570505990623620188996074, 1)"'
              '      }'
              '    },'
              '    "tagged_complex": {},'
              '    "untagged_real": {},'
              '    "intermediate_uids": {}'
              '  }</gtcArchiveJSON>'
              '</serialised>')
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    assert xml.is_valid()


@pytest.mark.parametrize(
    'value',
    ['',
     '  ',
     '\t',
     '\n',
     '\r',
     '\n\r',
     '\n\n\n\n',
     '\t\t\t\t\t',
     ' \t     \n                ',
     'does not matter!',
     '\n\n{"CLASS": "Archive"}\n\n'
     ])
def test_json_format_anything(xml, value):
    # The schema does not validate the JSON content, so can be any string with any attributes
    choice = f'<serialised><gtcArchiveJSON apple="red">{value}</gtcArchiveJSON></serialised>'
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    assert xml.is_valid()
