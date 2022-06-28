from Study.xml.xml_read import XML_READ
import xml.etree.ElementTree as ET

TAGS = ['.//{*}StudyDate', './/{*}StartStudy', './/{*}EndStudy', './/{*}TotalStudy', './/{*}TotalValidSleep',
        './/{*}SleepLatency', './/{*}REMLatency']

# TH for Totalstudy: 4 hr (= 14400 sec)
# TH for TotalValidSleep: less than 4 hr moderate, less than 1.5 hr (5400 sec) severe
MAINREPORT_TH = {'TotalStudy': 14400, 'TotalValidSleep_moderate': 14400, 'TotalValidSleep_severe': 5400}


class XML_REPORT(XML_READ):
    def __init__(self, files_path):
        super().__init__(files_path, TAGS, MAINREPORT_TH)

    def parse_xml(self):
        """
        this function parses MainReport.xml
        :return: dict of the parameters in MainReport.xml and the study status
        """
        mytree = ET.parse(self.files_path)
        myroot = mytree.getroot()
        for tag in self.xml_tags:
            x = myroot.findall(tag)
            if not x == []:
                self.results_dict[tag[6:]] = x[0].text  # tag[6:] is for cutting the './/{*}' in the start of tag
        for k, v in self.results_dict.items():
            self.check_threshold(k, v, self.thresholds_dct)
        return self.results_dict, self.status

    def check_threshold(self, k, v, th_dct):
        """
        this function checks for each key in the following cases if they are above/below a threshold
        :param k: key (field) in MainReport.xml file
        :param v: the appropriate value in statistics.xml file
        :param th_dct: dict of thresholds to check on the specific fields
        """
        match k:
            case 'TotalStudy':
                total_study_num_list = [int(s) for s in v.split() if s.isdigit()]  # extracts time from str
                total_study_sec = total_study_num_list[0] * 3600 + total_study_num_list[1] * 60  # convert to sec
                # less than 4 hr - raise a flag
                if total_study_sec < th_dct['TotalStudy']:
                    self.results_dict['TotalStudy'] = [v, 'TotalStudy Problem']
                    self.status = False

            case 'TotalValidSleep':
                valid_sleep_num_list = [int(s) for s in v.split() if s.isdigit()]  # extracts time from str
                valid_sleep_sec = valid_sleep_num_list[0] * 3600 + valid_sleep_num_list[1] * 60  # convert to sec
                # less than 4 hr moderate, less than 1.5 hr severe
                if th_dct['TotalValidSleep_severe'] < valid_sleep_sec < th_dct['TotalValidSleep_moderate']:
                    self.results_dict['TotalValidSleep'] = [v, 'TotalValidSleep moderate']
                    self.status = False
                if valid_sleep_sec < th_dct['TotalValidSleep_severe']:
                    self.results_dict['TotalValidSleep'] = [v, 'TotalValidSleep severe']
                    self.status = False

