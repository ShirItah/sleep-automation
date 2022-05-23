from xml.etree import cElementTree as ElementTree
from pprint import pprint


def main():
    xmlTree = ElementTree.parse("../studies/results/study1/statistics.xml")
    xmlRoot = xmlTree.getroot()
    dictRoot = xml_to_dict(xmlRoot, {})
    result = {xmlRoot.tag: dictRoot}
    pprint(dictRoot)
    print("------------")
    pprint(result)


def xml_to_dict(xml, result):
    notRelevantInfo = ["physician", "ZipCode", "WorkPhone", "Weight", "UniquePatientIdentification", 'BirthDay',
                       'City', 'Country', 'EpworthScore', 'Height', 'HistoryDisease', 'HomePhone', 'Medication',
                       'MobilePhone', 'NeckSize', 'Pacemaker', 'Pager', 'Sex', 'State', 'Street']
    for child in xml:

        if child.tag in notRelevantInfo:
            continue

        if len(child) == 0:
            result[child.tag] = child.text
        else:
            result[child.tag] = xml_to_dict(child, {})
    return result


if __name__ == '__main__':
    main()
