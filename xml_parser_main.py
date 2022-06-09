# Imports
from Study.Study import Study
from Study.xml.xml_stat import XML_STAT
from Study.xml.xml_report import XML_REPORT
from Study.xml.xml_stages import XML_STAGES
from zipfile import ZipFile
from Utilities.call_bat import WPI
import os
import json
import csv
from pprint import pprint


def main():
    """
    Main function
    calls the function that running WPI Analyze&Report, unzip the files and extracting the data
    """
    studies = ".\\studies\\test2\\source"
    dest = ".\\studies\\test2\\dest"

    WPI.analyze_report_caller(studies, dest)
    unzip_xmls(dest)

    for subdir, dirs, files in os.walk(dest):
        if not files == []:
            study_obj = get_object_list(subdir, files)
            pprint(study_obj.__dict__)

    # save_csv(study_obj)


def unzip_xmls(rootdir):
    """
    This function unzip xmls
    WPI extract to rootdir files for each study, which contain reprotfiles.zip file
    This function first unzip reporotfiles.zip
    then it unzip study.zip file that was extracted from reportfiles.zip
    """
    study_zip_ending = '\\study.zip'

    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            if not file.endswith('.zip'):
                continue
            zip_folder = os.path.join(subdir, file)  # path of the files extracted by WPI + FileName
            zip_path = os.path.dirname(zip_folder)  # target dir for xml files

            # unzip reportfiles.zip & unzip study.zip
            with ZipFile(zip_folder) as zip_ref1:
                zip_ref1.extractall(zip_path)
            with ZipFile(zip_path + study_zip_ending) as zip_ref2:
                zip_ref2.extractall(zip_path)


def get_object_list(subdir, files):
    """
    this function creates xml objects
    according to their type it calls the specific class and creates the object
    :param subdir: the path of each result folder
    :param files: the files in each folder that need to be parsed
    @returns xml object
    """
    zpt_files = ["Actigraph.zpt",  "PatAmplitude.zpt", "PAT_Infra.zpt", "PeripheralBP.zpt", "HeartRate.zpt", "SaO2.zpt",
                 "SBP_AC.zpt", "SnoreWP.zpt"]

    study = Study()
    for file in files:
        files_path = os.path.join(subdir, file)
        if file == "statistics.xml":
            study.stats = XML_STAT(files_path)
        elif file == "MainReport.xml":
            study.report = XML_REPORT(files_path)
        elif file == "SleepStagesChart.xml":
            study.stages = XML_STAGES(files_path)
        elif file in zpt_files:
            study.setZptAttribute(files_path, file)
        else:
            continue
    return study


def save_csv(obj_list):
    """
    this function saves the results_dict in csv file
    in ths csv file: each column is a key; each row is a study; each cell contains the val of the key
    :param obj_list: list of all objects (classes stat, report, stages)
    """
    csv_file_name = 'Resources/studies_params.csv'
    all_studies = list()

    for obj in obj_list:
        all_studies.append(obj.results)
    with open('dict.json', 'w') as d_j:
        json.dump(all_studies, d_j, indent=6)
    fieldnames = list(all_studies[1].keys())
    with open(csv_file_name, 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for study_param in all_studies:
            writer.writerow(study_param)


if __name__ == '__main__':
    main()
