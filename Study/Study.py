from Study.zpt.ZPTclass import ZPTclass as Zpt


class Study(Zpt):
    def __init__(self):
        super(Study, self).__init__()
        self._report = None
        self._stats = None
        self._stages = None
        self.study_Status = "OK"
        self.study_paths = []

    @property
    def report(self):
        return self._report

    @report.setter
    def report(self, value):
        self._report, status = value.parse_xml()
        self.set_status(status)

    @property
    def stats(self):
        return self._stats

    @stats.setter
    def stats(self, value):
        self._stats, status = value.parse_xml()
        self.set_status(status)

    @property
    def stages(self):
        return self._stages

    @stages.setter
    def stages(self, value):
        self._stages, status = value.parse_xml()
        self.set_status(status)

    def setZptAtribute1(self, pathZpt, name):
        self.setZptAtribute(pathZpt, name)

    def set_status(self, status):
        if status is False or self.status_zpt is False:
            self.study_Status = "NOT OK"

