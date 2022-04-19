from xml_read import XML_READ
import xml.etree.ElementTree as ET


class XML_STAGES(XML_READ):
    def __init__(self, zip_folder, xml_tags, thresholds_dct):
        super().__init__(zip_folder, xml_tags, thresholds_dct)


    def parse_xml(self):
        mytree = ET.parse(self.zip_folder)
        myroot = mytree.getroot()
        for tag in self.xml_tags:
            x = myroot.findall(tag)
            self.results_dict[tag[6:]] = x[0].text      # tag[6:] is for cutting the './/{*}' in the start of tag
        self.results_dict = {f'{k}[%]': v for k, v in self.results_dict.items()}            # adding units (percentage)
        for k, v in self.results_dict.items():
            res_dict = self.check_threshold_stages(k, v, self.thresholds_dct)
        return res_dict


    def check_threshold_stages(self, k, v, th_dct):
        """
        this function checks for each key in the following cases if they are above/below a threshold
        :param k: key (field) in statistics.xml file
        :param v: the appropriate value in statistics.xml file
        :param th_dct: dict of thresholds to check on the specific fields
        :return: dict of the parameters in statistics.xml with notes on the thresholds
        """
        match k:
            case 'Wake[%]':
                # more than 30%
                if float(v) > th_dct['Wake[%]']:
                    self.results_dict['Wake[%]'] = [v, 'Wake[%] Problem']
            case 'REM[%]':
                # less than 5%
                if float(v) < th_dct['REM[%]']:
                    self.results_dict['REM[%]'] = [v, 'REM[%] Problem']
        return self.results_dict