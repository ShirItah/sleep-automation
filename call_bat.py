import subprocess


def call_bat():
    # study = "C:\\Users\\RYair\\Des1ktop\\cliChecker\\study"
    # dest = "C:\\Users\\RYair\\Desktop\\cliChecker\\results"
    # action = "a"

    study = "C:\\Users\\ishir\\Desktop\\WPI_night_studies_auto_tool\\source\\study1"
    dest = "C:\\Users\\ishir\\Desktop\\WPI_night_studies_auto_tool\\results\\study10"
    action = "f"
    # str(random.randrange(0, 20)) -> example for first parm

    item = subprocess.Popen(["test.bat", study, dest, action],
                            shell=True, stdout=subprocess.PIPE)

    for idx, item in enumerate(item.stdout):
        print(idx, ':', item.decode())


