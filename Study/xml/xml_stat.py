from Study.xml.xml_read import XML_READ
import xml.etree.ElementTree as ET
import datetime
import itertools
from pprint import pprint

# Global variables
Parent = []

Patient = ['Email', 'FirstName', 'ID', 'LastName']

General = ['BraceletID', 'BraceletSN', 'DeviceSN', 'HardwareVersion', 'NumberOfNights', 'PaymentCode', 'Warnings',
           'SoftwareVersion', 'StudyDate', 'StudyStatus']

Parameters = ["AHI", "AHICentral", "AHI_4_Percent", "NREM_AHI", "NREM_ODI", "NREM_RDI", "RDI", "REM_AHI", "REM_ODI",
              "REM_RDI", "ODI", "NumberOfMixedApneas", "NumberOfMixedApneas_4_Percent", "TotalNumberOfApneas",
              "NumberOfWakes"]

PulseRate = ["MaxPRSleep", "MeanPRSleep", "MinPRSleep"]

Sat = ["Desats10_9", "Desats2_3", "Desats4_9", "DesatsAbove20", "MaxSatValue", "MeanNadirDesaturations", "MeanSatValue",
       "MinSatValue", "NumberOfDesaturations", "SatBelow70", "SatBelow80", "SatBelow85", "SatBelow88", "SatBelow90",
       "SatBelowEqual88"]

SBP = ["CSR_Percent", "Left_AHI", "Left_ODI", "Left_RDI", "MeanSnoreDB","NonSupine_AHI", "NonSupine_ODI", "NonSupine_RDI",
       "NumberOfCentralAH", "Prone_AHI", "Prone_ODI", "Prone_RDI", "REM_AHICentral", "Right_AHI", "Right_ODI",
       "Right_RDI", "SleepDuringLeft", "SleepDuringNonSupine", "SleepDuringProne", "SleepDuringRight",
       "SleepDuringSupine", "SnoreAbove40", "SnoreAbove50", "SnoreAbove60", "SnoreAbove70", "SnoreAbove80",
       "SnoreThreshold", "Supine_AHI", "Supine_ODI", "Supine_RDI", "NREM_AHICentral", "SleepOverThreshold"]

Time = ["TotalApneaSleepTime", "TotalArousalSleepTime", "TotalDeepSleepTime", "TotalLightSleepTime", "TotalREMTime",
        "TotalSleepTime", "TotalWakeTime"]

Analysis = dict(Patient={}, General={}, Parameters={}, PulseRate={}, Sat={}, SBP={}, Time={})

TIME_PARAMS = dict(SBP=['SleepOverThreshold', 'SnoreAbove40', 'SnoreAbove50', 'SnoreAbove60', 'SnoreAbove70',
                        'SnoreAbove80', 'SleepDuringProne', 'SleepDuringSupine', 'SleepDuringLeft', 'SleepDuringRight',
                        'SleepDuringNonSupine'],
                   Sat=['SatBelow90', 'SatBelowEqual88', 'SatBelow88', 'SatBelow85', 'SatBelow80', 'SatBelow70'],
                   Time=Time)

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
        self.dictRoot =None

    def parse_xml(self):
        """
        this function parses Statistics.xml
        it calls xml_to_dict() that parser the xml recursively
        :return: dict of the parameters in Statistics.xml and the study status
        """

        mytree = ET.parse(self.files_path)
        myroot = mytree.getroot()
        self.dictRoot = self.xml_to_dict(myroot, {})
        self.results_dict = {myroot.tag: self.dictRoot}
        # self.results_dict = self.time_delta()
        self.check_threshold(self.thresholds_dct)
        print(self.results_dict)
        return self.results_dict, self.status

    def xml_to_dict(self, xml, result):
        """
        this function parser statistics.xml recursively
        :param result:
        :param xml: myroot (study object)
        :return: dict of the parameters in Statistics.xml
        """
        Parent.append(xml.tag)
        for child in xml:

            if child.tag in self.notRelevantInfo:
                continue

            if len(child) == 0:
                if child.tag in General:
                    Analysis["General"][child.tag] = child.text
                match Parent[-1]:
                    case "patient":
                        if child.tag not in General:
                            Analysis["Patient"][child.tag] = child.text
                    case "analysis":
                        if child.tag in Parameters:
                            Analysis["Parameters"][child.tag] = child.text
                        elif child.tag in PulseRate:
                            Analysis["PulseRate"][child.tag] = child.text
                        elif child.tag in Sat:
                            Analysis["Sat"][child.tag] = child.text
                        elif child.tag in SBP:
                            Analysis["SBP"][child.tag] = child.text
                        elif child.tag in Time:
                            Analysis["Time"][child.tag] = child.text
                result.update(Analysis)
            else:
                self.xml_to_dict(child, {})
        return result

    def time_delta(self):
        """
        this function convert the values representing time from sec to hr,min,sec
        :return: dict of the parameters in Statistics.xml
        """
        for val in self.results_dict.values():
            for k, v in val.items():
                match k:
                    case "SBP":
                        for SBP_key in v.keys():
                            if SBP_key in self.time_params['SBP']:
                                if v[SBP_key] and v[SBP_key] != 'N/A':
                                    v[SBP_key] = str(datetime.timedelta(seconds=int(v[SBP_key])))
                    case "Sat":
                        for Sat_key in v.keys():
                            if Sat_key in self.time_params['Sat']:
                                if v[Sat_key] and v[Sat_key] != 'N/A':
                                    v[Sat_key] = str(datetime.timedelta(seconds=int(v[Sat_key])))
                    case "Time":
                        for Time_key in v.keys():
                            if Time_key in self.time_params['Time']:
                                if v[Time_key] and v[Time_key] != 'N/A':
                                    v[Time_key] = str(datetime.timedelta(seconds=int(v[Time_key])))
        # return self.results_dict

    def check_threshold(self, th_dct):
        """
        this function checks for each key in the following cases if they are above/below a threshold
        :param k: key (field) in statistics.xml file
        :param v: the appropriate value in statistics.xml file
        :param th_dct: dict of thresholds to check on the specific fields
        :return: dict of the parameters in statistics.xml with notes on the thresholds
        """
        for val in self.results_dict.values():
            for k, v in val.items():
                match k:
                    case "Parameters":
                        for Param_key, Param_val in v.items():
                            match Param_key:
                                case 'AHI':
                                    # between 5-15 - mild
                                    if th_dct['AHI_mild_s'] < float(Param_val) < th_dct['AHI_mild_moderate']:
                                        v["AHI"] = [Param_val, 'AHI - mild']
                                        self.status = False
                                    # between 15-30 - moderate
                                    if th_dct['AHI_mild_moderate'] < float(Param_val) < th_dct['AHI_moderate_severe']:
                                        v["AHI"] = [Param_val, 'AHI - moderate']
                                        self.status = False
                                    # larger than 30 - severe
                                    if float(Param_val) > th_dct['AHI_moderate_severe']:
                                        v["AHI"] = [Param_val, 'AHI - severe']
                                        self.status = False


