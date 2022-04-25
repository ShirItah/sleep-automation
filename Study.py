from ZPTclass import ZPTclass as Zpt


class Study(Zpt):
    def __init__(self):
        super(Study, self).__init__()
        self._report = None
        self._stats = None
        self._stages = None
        self.results = dict()

    @property
    def report(self):
        return self._report

    @report.setter
    def report(self, value):
        self.results.update(value.parse_xml())
        self._report = value

    @property
    def stats(self):
        return self._stats

    @stats.setter
    def stats(self, value):
        self.results.update(value.parse_xml())
        self._stats = value

    @property
    def stages(self):
        return self._stages

    @stages.setter
    def stages(self, value):
        self.results.update(value.parse_xml())
        self._stages = value
