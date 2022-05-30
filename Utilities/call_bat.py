import subprocess
import os
import datetime

bat_path = "C:\\Users\\ishir\\PycharmProjects\\sleep-automation\\Resources\\test.bat"


class WPI:
    def __init__(self):
        pass

    @staticmethod
    def call_bat(study, dest):
        print("call_bat")
        action = "f"
        print(study, dest)
        item = subprocess.Popen([bat_path, study, dest, action],
                                shell=True, stdout=subprocess.PIPE)
        print(111111)
        for idx, item in enumerate(item.stdout):
            print(idx, ':', item.decode())

            if item.decode()[:-3] == 'Parsing data completed OK':
                stamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S%f')  # timestamp for successful folder name
                os.rename(study, study + '_Done_' + stamp)  # rename source folder to show it was parsed successfully
                os.rename(dest, dest + '_Done_' + stamp)  # rename dest folder to show it was parsed successfully

    @classmethod
    def analyze_report_caller(cls, studies, dest):
        day = datetime.datetime.today().strftime('%Y_%m_%d')
        count = 0
        newPath = os.path.join(dest, day)  # folder name string for today
        if not os.path.exists(newPath):  # check if already created folder today, if not create one
            os.makedirs(newPath)

        for folder in os.listdir(studies):
            if count == 0:
                break
            currFolder = os.path.join(studies, folder)  # Concat studies with current subfolder
            files = os.listdir(currFolder)  # files in current subfolder

            # check if sleep.dat and patient.date exist. Used upper to be case-insensitive
            if "Patient.dat".upper() in (file.upper() for file in files) and \
                    "Sleep.dat".upper() in (file.upper() for file in files):
                WPI.call_bat(currFolder, os.path.join(newPath, folder))
            else:
                print("Patient.dat and\\or Sleep.dat are missing in", folder)
            count += 1


if __name__ == '__main__':
    studies = "C:\\Users\\ishir\\PycharmProjects\\sleep-automation\\studies\\source"
    dest = "C:\\Users\\ishir\\PycharmProjects\\sleep-automation\\studies\\results1"
    WPI.analyze_report_caller(studies, dest)
