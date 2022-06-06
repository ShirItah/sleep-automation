from Study.xml.xml_read import XML_READ
import xml.etree.ElementTree as ET

TAGS = ['.//{*}Wake', './/{*}Sleep', './/{*}REM', './/{*}NREM', './/{*}Light', './/{*}Deep']

# TH for wake [%]: > 30 %; TH for REM [%]: < 5%
STAGES_TH = {'Wake[%]': 30, 'REM[%]': 5}

class XML_STAGES(XML_READ):
    def __init__(self, files_path):
        super().__init__(files_path, TAGS, STAGES_TH)

    def parse_xml(self):
        """
        this function parses SleepStagesChart.xml and adding units (%) to the values
        :return: dict of the parameters in SleepStagesChart.xml and the study status
        """
        mytree = ET.parse(self.files_path)
        myroot = mytree.getroot()
        for tag in self.xml_tags:
            x = myroot.findall(tag)
            self.results_dict[tag[6:]] = x[0].text      # tag[6:] is for cutting the './/{*}' in the start of tag
        self.results_dict = {f'{k}[%]': v for k, v in self.results_dict.items()}            # adding units (percentage)
        for k, v in self.results_dict.items():
            self.check_threshold(k, v, self.thresholds_dct)
        return self.results_dict, self.status

    def check_threshold(self, k, v, th_dct):
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
                    self.status = False
            case 'REM[%]':
                # less than 5%
                if float(v) < th_dct['REM[%]']:
                    self.results_dict['REM[%]'] = [v, 'REM[%] Problem']
                    self.status = False
