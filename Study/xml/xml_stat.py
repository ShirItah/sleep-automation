from Study.xml.xml_read import XML_READ
import xml.etree.ElementTree as ET
import datetime
import itertools

# Global variables
TIME_PARAMS = ['SleepOverThreshold', 'SnoreAbove40', 'SnoreAbove50', 'SnoreAbove60', 'SnoreAbove70', 'SnoreAbove80',
               'SleepDuringProne', 'SleepDuringSupine', 'SleepDuringLeft', 'SleepDuringRight', 'SleepDuringNonSupine',
               'TotalApneaSleepTime', 'TotalWakeTime', 'TotalSleepTime', 'TotalArousalSleepTime', 'TotalREMTime',
               'TotalDeepSleepTime', 'TotalLightSleepTime', 'SatBelow90', 'SatBelowEqual88', 'SatBelow88', 'SatBelow85',
               'SatBelow80', 'SatBelow70']

NOT_RELEVANT = ['BirthDay', 'BraceletMessage', 'BraceletStudy', 'City', 'Comments', 'Country', 'Coverage',
                'EpworthScore', 'Height', 'HistoryDisease', 'HomePhone', 'Medication', 'MobilePhone', 'NeckSize',
                'Pacemaker', 'Pager', 'Sex', 'SnoreBPChart_Y_axis', 'SnoreDb_Y_axis', 'StagesChart_Y_axis', 'State',
                'Street', 'StudyEndTime', 'StudyStartTime', 'TotalAH_CentralValidSleepTime',
                'UniquePatientIdentification', 'Weight', 'WorkPhone', 'ZipCode', 'physician']

# TH for AHI: between 5-15 mild, between 15-30 moderate, larger than 30 severe
STAT_TH = {'AHI_mild_s': 5, 'AHI_mild_moderate': 15, 'AHI_moderate_severe': 30}


class XML_STAT(XML_READ):
    def __init__(self, files_path):
        super().__init__(files_path, [], STAT_TH)
        self.time_params = TIME_PARAMS
        self.notRelevantInfo = NOT_RELEVANT

    def parse_xml(self):
        """
        this function parses Statistics.xml
        it calls xml_to_dict() that parser the xml recursively
        :return: dict of the parameters in Statistics.xml and the study status
        """
        mytree = ET.parse(self.files_path)
        myroot = mytree.getroot()
        self.results_dict = self.xml_to_dict(myroot)
        # self.results_dict = self.time_delta()
        for k, v in self.results_dict.items():
            self.check_threshold(k, v, self.thresholds_dct)
        return self.results_dict, self.status

    def xml_to_dict(self, xml):
        """
        this function parser statistics.xml recursively
        :param xml: myroot (study object)
        :return: dict of the parameters in Statistics.xml
        """
        for child in xml:
            if child.tag in self.notRelevantInfo:
                continue
            if len(child) == 0:
                self.results_dict[child.tag] = child.text
            else:
                self.results_dict[child.tag] = self.xml_to_dict(child)
        return self.results_dict

    def time_delta(self):
        """
        this function convert the values representing time from sec to hr,min,sec
        :return: dict of the parameters in Statistics.xml
        """
        time_param_dict = dict((k, self.results_dict[k]) for k in self.time_params)
        for time_k, time_v in itertools.zip_longest(self.time_params, time_param_dict.values()):
            if time_v and time_v != 'N/A':
                self.results_dict[time_k] = str(datetime.timedelta(seconds=int(time_v)))
        return self.results_dict

    def check_threshold(self, k, v, th_dct):
        """
        this function checks for each key in the following cases if they are above/below a threshold
        :param k: key (field) in statistics.xml file
        :param v: the appropriate value in statistics.xml file
        :param th_dct: dict of thresholds to check on the specific fields
        :return: dict of the parameters in statistics.xml with notes on the thresholds
        """
        match k:
            case 'AHI':
                # between 5-15 - mild
                if th_dct['AHI_mild_s'] < float(v) < th_dct['AHI_mild_moderate']:
                    self.results_dict['AHI'] = [v, 'AHI - mild']
                    self.status = False
                # between 15-30 - moderate
                if th_dct['AHI_mild_moderate'] < float(v) < th_dct['AHI_moderate_severe']:
                    self.results_dict['AHI'] = [v, 'AHI - moderate']
                    self.status = False
                # larger than 30 - severe
                if float(v) > th_dct['AHI_moderate_severe']:
                    self.results_dict['AHI'] = [v, 'AHI - severe']
                    self.status = False
