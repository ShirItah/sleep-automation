class XML_READ:
    def __init__(self, zip_folder, xml_tags, thresholds_dct):
        self.zip_folder = zip_folder
        self.xml_tags = xml_tags
        self.thresholds_dct = thresholds_dct
        self.results_dict = dict()
        # self.ANALYSIS_PARAMS_NUM_NO_SBP = ["RDI", "AHI", "ODI", "REM_RDI", "REM_AHI", "REM_ODI", "NREM_RDI", "NREM_AHI",
        #                                    "NREM_ODI",
        #                                    "TotalNumberOfApneas", "AHICentral", "CSR_Percent", "REM_AHICentral",
        #                                    "NREM_AHICentral",
        #                                    "NumberOfCentralAH", "NumberOfWakes"]
