from xml_read import XML_READ
import xml.etree.ElementTree as ET


class XML_REPORT(XML_READ):
    def __init__(self, zip_folder, xml_tags):
        super().__init__(zip_folder, xml_tags)

    def parse_xml(self):
        mytree = ET.parse(self.zip_folder)
        myroot = mytree.getroot()
        for tag in self.xml_tags:
            x = myroot.findall(tag)
            self.results_dict[tag[6:]] = x[0].text      # tag[6:] is for cutting the './/{*}' in the start of tag
        return self.results_dict
