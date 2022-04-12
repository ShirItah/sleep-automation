from xml_read import XML_READ
import xml.etree.ElementTree as ET
from pprint import pprint


class XML_REPORT(XML_READ):
    def __init__(self, zip_folder, xml_tags, thresholds_dct):
        super().__init__(zip_folder, xml_tags)
        self.thresholds_dct = thresholds_dct

    def parse_xml(self):
        mytree = ET.parse(self.zip_folder)
        myroot = mytree.getroot()
        for tag in self.xml_tags:
            x = myroot.findall(tag)
            self.results_dict[tag[6:]] = x[0].text  # tag[6:] is for cutting the './/{*}' in the start of tag
        for k, v in self.results_dict.items():
            res_dict = self.check_threshold_main_report(k, v, self.thresholds_dct)
        return res_dict

    def check_threshold_main_report(self, k, v, th_dct):
        """
        this function checks for each key in the following cases if they are above/below a threshold
        :param k: key (field) in statistics.xml file
        :param v: the appropriate value in statistics.xml file
        :param th_dct: dict of thresholds to check on the specific fields
        :return: dict of the parameters in statistics.xml with notes on the thresholds
        """
        match k:
            case 'TotalStudy':
                total_study_num_list = [int(s) for s in v.split() if s.isdigit()]  # extracts time from str
                total_study_sec = total_study_num_list[0] * 3600 + total_study_num_list[1] * 60  # convert to sec
                # less than 4 hr - raise a flag
                if total_study_sec < th_dct['TotalStudy']:
                    self.results_dict['TotalStudy'] = [v, 'TotalStudy Problem']
            case 'TotalValidSleep':
                valid_sleep_num_list = [int(s) for s in v.split() if s.isdigit()]  # extracts time from str
                valid_sleep_sec = valid_sleep_num_list[0] * 3600 + valid_sleep_num_list[1] * 60  # convert to sec
                # less than 4 hr moderate, less than 1.5 hr severe
                if th_dct['TotalValidSleep_severe'] < valid_sleep_sec < th_dct['TotalValidSleep_moderate']:
                    self.results_dict['TotalValidSleep'] = [v, 'TotalValidSleep TotalValidSleep moderate']
                if valid_sleep_sec < th_dct['TotalValidSleep_severe']:
                    self.results_dict['TotalValidSleep'] = [v, 'TotalValidSleep TotalValidSleep severe']
        return self.results_dict
