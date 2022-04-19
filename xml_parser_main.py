# Before running this script:
# Launch CMD window
# Run the command:
# C:\Program Files (x86)\Itamar medical\WP_Interface > zzzPATAnalyzeReport.exe –s “source folder”
# –d “destination folder” –a f –p

####### Imports #######
import json
from xml_stat import XML_STAT
from xml_report import XML_REPORT
from xml_stages import XML_STAGES
from ZPTclass import ZPTclass
from xml_reg import XML_REG
import os
import zipfile
from pprint import pprint
import csv
####### Global variables #########

## Parameters lists in statistics.xml - "analysis" tag
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

## XML Files name & Tags
# statistics content declaration
STAT_NAME_TAGS = ("statistics.xml", [("patient", ["ID", "FirstName", "LastName"]),
                                     ("analysis", ANALYSIS_ALL_PARAMS),
                                     ("HardwareVersion", []),
                                     ("SoftwareVersion", []),
                                     ("DeviceSN", [])])

# main report content declaration
MAINREPORT_NAME_TAGS = ("MainReport.xml", [".//{*}StudyDate", ".//{*}StartStudy",
                                           ".//{*}EndStudy", ".//{*}TotalStudy", ".//{*}TotalValidSleep",
                                           ".//{*}MeanSatValue", ".//{*}MinSatValue",
                                           ".//{*}MaxSatValue", ".//{*}MeanNadirDesaturations", ".//{*}SleepLatency",
                                           ".//{*}REMLatency", ".//{*}NumberOfWakes"])

# Sleep Stages Chart content declaration
SLEEP_STAGES_NAME_TAGS = ('SleepStagesChart.xml', [".//{*}Wake", ".//{*}Sleep", ".//{*}REM", ".//{*}NREM",
                                                   ".//{*}Light", ".//{*}Deep"])


## Thresholds
# Statistics Thresholds
# TH for AHI: between 5-15 mild, between 15-30 moderate, larger than 30 severe

STAT_TH = {'AHI_mild_s': 5, 'AHI_mild_moderate': 15, 'AHI_moderate_severe': 30}

# MainReport Thresholds
# TH for Totalstudy: 4 hr (= 14400 sec)
# TH for TotalValidSleep: less than 4 hr moderate, less than 1.5 hr (5400 sec) severe
# TH for SpO2: check durations of "satBelow-x" - TODO: extract from zpt files

MAINREPORT_TH = {'TotalStudy': 14400, 'TotalValidSleep_moderate': 14400, 'TotalValidSleep_severe': 5400}

# Stages Thresholds
# TH for wake [%]: > 30 %
# TH for REM [%]: < 5%

STAGES_TH = {'Wake[%]': 30, 'REM[%]': 5}

# Thresholds list
ALL_TH = [STAT_TH, MAINREPORT_TH, STAGES_TH]

## ZPT files list
ZPT_FILES = ["Actigraph.zpt", "PAT_Infra.zpt", "PeripheralBP.zpt", "SaO2.zpt", "PatAmplitude.zpt"]


## Directory of the WPI output & unzip function outputs
ROOTDIR = '.\\studies\\results'

## The ending of the zip file containing all the xmls
STUDY_ZIP_ENDING = '\\study.zip'

## CSV file name
CSVFILE = 'studies_params.csv'

## ZPT data file name
ZPT_TXT = 'zpt_data.txt'


def main():
    """
    Main function
    """
    unzip_xmls(ROOTDIR)
    list_of_studies_xml_obj = get_object_list(ROOTDIR)
    studies_dicts_list = parse_xmls(list_of_studies_xml_obj)
    # pprint(studies_dicts_list)
    read_zpt(ROOTDIR, ZPT_FILES)
    save_csv(studies_dicts_list, CSVFILE)


def unzip_xmls(rootdir):
    """
    This function unzip xmls
    WPI extract to rootdir files for each study, which contain reprotfiles.zip file
    This function first unzip reporotfiles.zip
    then it unzip study.zip file that was extracted from reportfiles.zip
    """
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            zip_folder = os.path.join(subdir, file)  # path of the files extracted by WPI + FileName
            zip_path = os.path.dirname(zip_folder)  # target dir for xml files
            if not zip_folder.endswith('.zip'):
                continue
            # unzip reportfiles.zip
            with zipfile.ZipFile(zip_folder) as zip_ref:
                zip_ref.extractall(zip_path)
            # unzip study.zip
            with zipfile.ZipFile(zip_path + STUDY_ZIP_ENDING) as zip_ref:
                zip_ref.extractall(zip_path)


def get_object_list(rootdir):
    """
    this function creates list of xml objects
    according to their type it calls the specific class and creates the object
    @param rootdir: the path of all the xml files
    @returns list of lists xml objects (for all the studies, each list is for different study)
    """
    list_of_xml_objs = list()  # list of xml objects per study
    list_of_xml_objs_copy = list()
    list_of_studies_xml_obj = list()  # list of lists - each list is for one study

    # for loop to read file by file
    for subdir, dirs, files in os.walk(rootdir):
        list_of_xml_objs.clear()
        if not files == []:
            for file in files:
                zip_folder = os.path.join(subdir, file)  # path of the files extracted by WPI+FileName
                if not file.endswith('.xml'):
                    continue
                if file == STAT_NAME_TAGS[0]:
                    current_xml = XML_STAT(zip_folder, STAT_NAME_TAGS[1], ANALYSIS_PARAMS_SBP, ANALYSIS_PARAMS_TIME_SBP,
                                           ANALYSIS_PARAMS_TIME_NO_SBP, ALL_TH[0])
                elif file == MAINREPORT_NAME_TAGS[0]:
                    current_xml = XML_REPORT(zip_folder, MAINREPORT_NAME_TAGS[1], ALL_TH[1])
                elif file == SLEEP_STAGES_NAME_TAGS[0]:
                    current_xml = XML_STAGES(zip_folder, SLEEP_STAGES_NAME_TAGS[1], ALL_TH[2])
                else:
                    continue

                list_of_xml_objs.append(current_xml)

                list_of_xml_objs_copy = list_of_xml_objs.copy()
                # current_xml.parse_xml()
            list_of_studies_xml_obj.append(list_of_xml_objs_copy)
    return list_of_studies_xml_obj


def parse_xmls(studies_xml_obj):
    """
    this function parses the necessary data from each xml according to def parse_xml in each class
    all the data is kept in dictionary; different dict for each class
    it combines all the dictionaries for each study and creates list of dicts
    @param studies_xml_obj: the list of all the xml objects
    @return: list of dicts contains the extracted data
    """
    studies_dicts_list = list()
    dest_dict = {}
    copy_dest_dict = {}
    for list_of_xml_objs in studies_xml_obj:
        dest_dict.clear()
        for xml_obj in list_of_xml_objs:
            result_dict = xml_obj.parse_xml()
            # pprint(result_dict)
            dest_dict.update(result_dict)
            copy_dest_dict = dict(dest_dict)
        studies_dicts_list.append(copy_dest_dict)
    return studies_dicts_list


def read_zpt(rootdir, zpt_files):
    data_mat = []
    ZPT_FILES = ["Actigraph.zpt", "PatAmplitude.zpt",  "PAT_Infra.zpt", "PeripheralBP.zpt", "SaO2.zpt", ]

    for subdir, dirs, files in os.walk(rootdir):
        data_mat.clear()
        if not files == []:
            # for file in files:
            #     if file in ZPT_FILES:
            #         print(file)
            #         zip_folder = os.path.join(subdir, file)
            #         zpt_data = ZPTclass(zip_folder, subdir, data_mat, ZPT_TXT, file)
            #         # zpt_data.write_zpt_to_txt()

            for zpt_file in zpt_files:
                for file in files:
                    if file != zpt_file:
                        continue
                    zip_folder = os.path.join(subdir, file)  # path of the files extracted by WPI+FileName
                    zpt_data = ZPTclass(zip_folder, subdir, data_mat, ZPT_TXT)



def save_csv(studies_list, csv_file_name):
    """
    this function saves the results_dict in csv file
    in ths csv file: each column is a key; each row is a study; each cell contains the val of the key
    :param csv_file_name: the name of the csv file that stores all the data
    :param studies_dicts_list: list of dictionaries for all the studies
    """
    with open('dict.json', 'w') as d_j:
        json.dump(studies_list, d_j, indent=6)
    fieldnames = list(studies_list[1].keys())
    with open(csv_file_name, 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for study_param in studies_list:
            writer.writerow(study_param)


if __name__ == '__main__':
    main()
