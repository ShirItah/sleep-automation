# Before running this script:
# Launch CMD window
# Run the command:
# C:\Program Files (x86)\Itamar medical\WP_Interface > zzzPATAnalyzeReport.exe –s “source folder”
# –d “destination folder” –a f –p

####### Imports #######

from xml_stat import XML_STAT
from xml_report import XML_REPORT
from xml_stages import XML_STAGES
from xml_reg import XML_REG
import os
import zipfile
from pprint import pprint
import csv

####### Global variables #########

## Parameters lists in statistics.xml - "analysis" tag
# Params list exists in all the studies
ANALYSIS_PARAMS = ["RDI", "AHI", "ODI", "REM_RDI", "REM_AHI", "REM_ODI", "NREM_RDI", "NREM_AHI", "NREM_ODI",
                   "TotalNumberOfApneas", "AHICentral", "CSR_Percent", "REM_AHICentral", "NREM_AHICentral",
                   "NumberOfCentralAH", "SatBelowEqual88", "SatBelowEqual88"]

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
ANALYSIS_ALL_PARAMS = ANALYSIS_PARAMS + ANALYSIS_PARAMS_SBP

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

# Regular files: contain vector of the values Vs time
# file1 - Heart Rate Vs Time
HR_NAME_TAGS = ("HeartRateTimeline.xml", [".//{*}SiTime", ".//{*}SiValue1"])

# file2 - PAT amplitude Vs Time
PATAMP_NAME_TAGS = ("PatAmplitudeTimeline.xml", [".//{*}SiTime", ".//{*}SiValuePatAmpl"])

# file3 - Saturation Vs Time
SAT_NAME_TAGS = ("SatPulseRate.xml", [".//{*}SiTime", ".//{*}SiValueSaO2"])

# file 4- Snoring Vs Time - for studies with SBP
SNORE_NAME_TAGS = ("SnoreBodyPositionTimeline.xml", [".//{*}SiTime", "//{*}SiValueSnore"])

# file5- Body position Vs Time - TODO: understand how to add this only to the studies containing SBP

# list of pair, XML File Names & Tags
# this list is only for the regular files
XML_REG_FILE_NAMES_AND_TAGS = [HR_NAME_TAGS, PATAMP_NAME_TAGS, SAT_NAME_TAGS, SNORE_NAME_TAGS]

# directory of the WPI output & unzip function outputs
ROOTDIR = '.\\WPI_night_studies_auto_tool\\results'

# the ending of the zip file containing all the xmls
STUDY_ZIP_ENDING = '\\study.zip'


def main():
    """
    Main function
    """
    unzip_xmls(ROOTDIR)
    list_of_studies_xml_obj = get_object_list(ROOTDIR)
    studies_dicts_list = parse_xmls(list_of_studies_xml_obj)
    #pprint(studies_dicts_list)
    save_csv(studies_dicts_list)


def unzip_xmls(ROOTDIR):
    """
    This function unzip xmls
    WPI extract to ROOTDIR files for each study, which contain reprotfiles.zip file
    This function first unzip reporotfiles.zip
    then it unzip study.zip file that was extracted from reportfiles.zip
    """
    for subdir, dirs, files in os.walk(ROOTDIR):
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


def get_object_list(ROOTDIR):
    """
    this function creates list of xml objects
    according to their type it calls the specific class and creates the object
    @param ROOTDIR: the path of all the xml files
    @returns list of lists xml objects (for all the studies, each list is for different study)
    """
    list_of_xml_objs = list()           # list of xml objects per study
    list_of_xml_objs_copy = list()
    list_of_studies_xml_obj = list()    # list of lists - each list is for one study

    # for loop to read file by file
    for subdir, dirs, files in os.walk(ROOTDIR):
        list_of_xml_objs.clear()
        if not files == []:
            for file in files:
                zip_folder = os.path.join(subdir, file)  # path of the files extracted by WPI+FileName
                if not file.endswith('.xml'):
                    continue
                if file == STAT_NAME_TAGS[0]:
                    current_xml = XML_STAT(zip_folder, STAT_NAME_TAGS[1], ANALYSIS_PARAMS_SBP, ANALYSIS_PARAMS_TIME_SBP)
                elif file == MAINREPORT_NAME_TAGS[0]:
                    current_xml = XML_REPORT(zip_folder, MAINREPORT_NAME_TAGS[1])
                elif file == SLEEP_STAGES_NAME_TAGS[0]:
                    current_xml = XML_STAGES(zip_folder, SLEEP_STAGES_NAME_TAGS[1])
                else:
                    continue
                # else:
                #     # loop to find the relevant xml in XML_REG_FILE_NAMES_AND_TAGS save index in i
                #     for i in XML_REG_FILE_NAMES_AND_TAGS:
                #         current_xml = XML_REG(zip_folder, XML_REG_FILE_NAMES_AND_TAGS[i][1])
                list_of_xml_objs.append(current_xml)
                list_of_xml_objs_copy = list_of_xml_objs.copy()
            list_of_studies_xml_obj.append(list_of_xml_objs_copy)
    return list_of_studies_xml_obj


def parse_xmls(list_of_studies_xml_obj):
    """
    this function parses the necessary data from each xml according to def parse_xml in each class
    all the data is kept in dictionary; different dict for each class
    it combines all the dictionaries for each study and creates list of dicts
    @param list_of_studies_xml_obj: the list of all the xml objects
    @return: list of dicts contains the extracted data
    """
    studies_dicts_list = list()
    dest_dict = {}
    copy_dest_dict = {}
    for list_of_xml_objs in list_of_studies_xml_obj:
        dest_dict.clear()
        for xml_obj in list_of_xml_objs:
            result_dict = xml_obj.parse_xml()
            dest_dict.update(result_dict)
            copy_dest_dict = dict(dest_dict)
        studies_dicts_list.append(copy_dest_dict)
    return studies_dicts_list


def save_csv(studies_dicts_list):
    """
    this function saves the results_dict in csv file
    in ths csv file: each column is a key; each row is a study; each cell contains the val of the key
    :param studies_dicts_list: list of dictionaries for all the studies
    """
    fieldnames = list(studies_dicts_list[1].keys())
    with open('studies_params.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for study_param in studies_dicts_list:
            writer.writerow(study_param)


if __name__ == '__main__':
    main()
