class XML_READ:
    def __init__(self, files_path, xml_tags, thresholds_dct):
        self.files_path = files_path
        self.xml_tags = xml_tags
        self.thresholds_dct = thresholds_dct
        self.results_dict = dict()
        self.status = True
