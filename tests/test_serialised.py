def test_no_choice(xml):
    choice = '<serialised/>'
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r'Expected is one of .*gtcArchive, .*gtcArchiveJSON')


def test_invalid_choice(xml):
    choice = '<serialised><invalid>some-random-text</invalid></serialised>'
    xml.calibrations(xml.measurand(xml.component(xml.report(choice=choice))))
    xml.raises(r'Expected is one of .*gtcArchive, .*gtcArchiveJSON')
