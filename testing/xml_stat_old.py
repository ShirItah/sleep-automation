from Study.xml.xml_read import XML_READ
import xml.etree.ElementTree as ET
import datetime
import itertools

# Global variables
NO_SBP_STUDY = "W/O SBP"
NO_SBP_PARAM_EXAMPLE = 'AHICentral'

# Params list exists in all the studies
# numeric parameters
ANALYSIS_PARAMS_NUM_NO_SBP = ["RDI", "AHI", "ODI", "REM_RDI", "REM_AHI", "REM_ODI", "NREM_RDI", "NREM_AHI", "NREM_ODI",
                              "TotalNumberOfApneas", "AHICentral", "CSR_Percent", "REM_AHICentral", "NREM_AHICentral",
                              "NumberOfCentralAH", "NumberOfWakes"]

# time parameters
ANALYSIS_PARAMS_TIME_NO_SBP = ["TotalApneaSleepTime", "TotalWakeTime", "TotalSleepTime", "TotalArousalSleepTime",
                               "TotalREMTime", "TotalDeepSleepTime", "TotalLightSleepTime", "SatBelow90",
                               "SatBelowEqual88", "SatBelow88", "SatBelow85", "SatBelow80", "SatBelow70"]

# combination of NO SBP parameters
ANALYSIS_PARAMS_NO_SBP = ANALYSIS_PARAMS_NUM_NO_SBP + ANALYSIS_PARAMS_TIME_NO_SBP

# Params list exists only in studies containing SBP
# numeric parameters
ANALYSIS_PARAMS_NUM_SBP = ["MeanSnoreDB", "Prone_RDI", "Prone_AHI", "Prone_ODI", "Supine_RDI", "Supine_AHI",
                           "Supine_ODI", "Left_RDI", "Left_AHI", "Left_ODI", "Right_RDI", "Right_AHI", "Right_ODI",
                           "NonSupine_RDI", "NonSupine_AHI", "NonSupine_ODI"]

# time parameters
ANALYSIS_PARAMS_TIME_SBP = ["SleepOverThreshold", "SnoreAbove40", "SnoreAbove50", "SnoreAbove60", "SnoreAbove70",
                            "SnoreAbove80", "SleepDuringProne", "SleepDuringSupine", "SleepDuringLeft",
                            "SleepDuringRight", "SleepDuringNonSupine"]

# combination of SBP parameters
ANALYSIS_PARAMS_SBP = ANALYSIS_PARAMS_NUM_SBP + ANALYSIS_PARAMS_TIME_SBP

# combination of all the parameters lists in statistics.xml
ANALYSIS_ALL_PARAMS = ANALYSIS_PARAMS_NO_SBP + ANALYSIS_PARAMS_SBP

TAGS = [("patient", ["ID", "FirstName", "LastName"]),
        ("analysis", ANALYSIS_ALL_PARAMS),
        ("HardwareVersion", []),
        ("SoftwareVersion", []),
        ("DeviceSN", []),
        ("BraceletSN", [])]

# TH for AHI: between 5-15 mild, between 15-30 moderate, larger than 30 severe
STAT_TH = {'AHI_mild_s': 5, 'AHI_mild_moderate': 15, 'AHI_moderate_severe': 30}


class XML_STAT(XML_READ):
    def __init__(self, files_path):
        super().__init__(files_path, TAGS, STAT_TH)
        self.sbp_tags = ANALYSIS_PARAMS_SBP
        self.sbp_tags_time = ANALYSIS_PARAMS_TIME_SBP
        self.no_sbp_tags_time = ANALYSIS_PARAMS_TIME_NO_SBP

    def parse_xml(self):
        """
        this function parses statistics.xml; dealing with different cases:
        the case that the necessary data is in tag (params list is empty)
        the case that the study is w/o SBP sensor:
        1) some params are not included, 2) the param is included, but it contains N/A
        => we want to replace 1),2) with "W/O SBP"
        for params containing seconds => convert to hr,min,sec
        :return: dict of the parameters in statistics.xml
        """
        mytree = ET.parse(self.files_path)
        myroot = mytree.getroot()
        for tag, params in self.xml_tags:
            x = myroot.findall(tag)
            if not params:  # in the cases that params is empty
                self.results_dict[tag] = x[0].text
            else:
                for param in params:
                    value = x[0].find(param)
                    if value is None:  # for studies w/o SBP, the case that fields don't exist
                        self.results_dict[param] = NO_SBP_STUDY
                    else:
                        self.results_dict[param] = x[0].find(param).text
        if self.results_dict[NO_SBP_PARAM_EXAMPLE] == NO_SBP_STUDY:  # for studies w/o SBP, the case that param=N/A
            for param_sbp in self.sbp_tags:
                self.results_dict[param_sbp] = NO_SBP_STUDY  # changing N/A to "NO_SBP_STUDY"
        else:
            # convert the values in sbp_tags_time (representing time) from sec to hr,min,sec
            sec_param_dict_sbp = dict((k, self.results_dict[k]) for k in self.sbp_tags_time)
            sec_params_sbp = list(sec_param_dict_sbp.values())
            # print(sec_param_dict_sbp)
            for param_time, sec_param in itertools.zip_longest(self.sbp_tags_time, sec_params_sbp):
                self.results_dict[param_time] = str(datetime.timedelta(seconds=int(sec_param)))
        # convert the values in no_sbp_tags_time (representing time) from sec to hr,min,sec
        sec_param_dict_no_sbp = dict((k, self.results_dict[k]) for k in self.no_sbp_tags_time)
        sec_params_no_sbp = list(sec_param_dict_no_sbp.values())
        for param_time, sec_param in itertools.zip_longest(self.no_sbp_tags_time, sec_params_no_sbp):
            if not sec_param == "N/A":
                self.results_dict[param_time] = str(datetime.timedelta(seconds=int(sec_param)))
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


