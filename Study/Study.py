from Study.zpt.ZPTclass import ZPTclass as Zpt


class Patient:
    def __init__(self):
        self.fname = None
        self.lname = None
        self.ID = None


class Study(Zpt, Patient):
    def __init__(self):
        super(Study, self).__init__()
        self._report = None
        self._stats = None
        self._stages = None
        self.study_Status = "OK"
        self.study_paths = []
        # self.results = dict()

    @property
    def report(self):
        return self._report

    @report.setter
    def report(self, value):
        self._report, status = value.parse_xml()
        self.set_status(status)
        # self.add_to_result(self._report)

    @property
    def stats(self):
        return self._stats

    @stats.setter
    def stats(self, value):
        self._stats, status = value.parse_xml()
        self.add_to_result(self._stats)
        self.set_status(status)
        self.ID = self._stats['ID']
        self.fname = self._stats['FirstName']
        self.lname = self._stats['LastName']

    @property
    def stages(self):
        return self._stages

    @stages.setter
    def stages(self, value):
        self._stages, status = value.parse_xml()
        self.add_to_result(self._stages)
        self.set_status(status)

    def setZptAtribute1(self, pathZpt, name):
        print("fhjabhadfhj")
        self.setZptAtribute(pathZpt, name)

    def add_to_result(self, dict):
        pass
        # self.results.update(dict)

    def get_data(self):
        return self.fname, self.lname, self.ID

    def set_status(self, status):
        if status or self.status_zpt is False:
            self.study_Status = "NOT OK"
