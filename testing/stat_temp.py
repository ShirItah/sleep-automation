from xml.etree import cElementTree as ElementTree
from pprint import pprint
from Study.stat.Patient import Patient

def main():
    xmlTree = ElementTree.parse("../studies/results/study1/statistics.xml")
    xmlRoot = xmlTree.getroot()
    dictRoot = xml_to_dict(xmlRoot, {}, obj=None)
    result = {xmlRoot.tag: dictRoot}
    pprint(dictRoot)
    print("------------")
    pprint(result)


def xml_to_dict(xml, result, obj):
    notRelevantInfo = ['BirthDay', 'BraceletMessage', 'BraceletStudy', 'City', 'Comments', 'Country', 'Coverage',
                'EpworthScore', 'Height', 'HistoryDisease', 'HomePhone', 'Medication', 'MobilePhone', 'NeckSize',
                'Pacemaker', 'Pager', 'Sex', 'SnoreBPChart_Y_axis', 'SnoreDb_Y_axis', 'StagesChart_Y_axis', 'State',
                'Street', 'StudyEndTime', 'StudyStartTime', 'TotalAH_CentralValidSleepTime',
                'UniquePatientIdentification', 'Weight', 'WorkPhone', 'ZipCode', 'physician']

    for child in xml:


        if child.tag in notRelevantInfo:
            continue

        if len(child) == 0:
            # print(child.tag)
            setattr(obj, child.tag, child.text)
            print(obj.ID)
            result[child.tag] = child.text
            # print(child.text)
        else:
            # print(child.tag)
            if child.tag == 'patient':
                obj = Patient()
                result[child.tag] = xml_to_dict(child, {}, obj)
    return result


if __name__ == '__main__':
    main()
