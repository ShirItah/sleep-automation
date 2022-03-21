from xml_read import XML_READ
import xml.etree.ElementTree as ET
import datetime
import itertools

## Global variables ##
NO_SBP_STUDY = "W/O SBP"
NO_SBP_PARAM_EXAMPLE = 'AHICentral'

class XML_STAT(XML_READ):
    def __init__(self, zip_folder, xml_tags, sbp_tags, sbp_tags_time, no_sbp_tags_time):
        super().__init__(zip_folder, xml_tags)
        self.sbp_tags = sbp_tags
        self.sbp_tags_time = sbp_tags_time
        self.no_sbp_tags_time = no_sbp_tags_time

    def parse_xml(self):
        """
        this function parses statistics.xml; dealing with different cases:
        the case that the necessary data is in tag (params list is empty)
        the case that the study is w/o SBP sensor:
        1) some params are not included, 2) the param is included, but it contains N/A
        => we want to replace 1),2) with "W/O SBP"
        for params containing seconds => convert to hr,min,sec
        :return: dict of the parameters in statistics.xml
        """
        mytree = ET.parse(self.zip_folder)
        myroot = mytree.getroot()
        for tag, params in self.xml_tags:
            x = myroot.findall(tag)
            if not params:                                      # in the cases that params is empty
                self.results_dict[tag] = x[0].text
            else:
                for param in params:
                    value = x[0].find(param)
                    if value is None:                           # for studies w/o SBP, the case that fields don't exist
                        self.results_dict[param] = NO_SBP_STUDY
                    else:
                        self.results_dict[param] = x[0].find(param).text
        if self.results_dict[NO_SBP_PARAM_EXAMPLE] == NO_SBP_STUDY:     # for studies w/o SBP, the case that param=N/A
            for param_sbp in self.sbp_tags:
                self.results_dict[param_sbp] = NO_SBP_STUDY             # changing N/A to "NO_SBP_STUDY"
        else:
            # convert the values in sbp_tags_time (representing time) from sec to hr,min,sec
            sec_param_dict_sbp = dict((k, self.results_dict[k]) for k in self.sbp_tags_time)
            sec_params_sbp = list(sec_param_dict_sbp.values())
            for param_time, sec_param in itertools.zip_longest(self.sbp_tags_time, sec_params_sbp):
                self.results_dict[param_time] = str(datetime.timedelta(seconds=int(sec_param)))
        # convert the values in no_sbp_tags_time (representing time) from sec to hr,min,sec
        sec_param_dict_no_sbp = dict((k, self.results_dict[k]) for k in self.no_sbp_tags_time)
        sec_params_no_sbp = list(sec_param_dict_no_sbp.values())
        for param_time, sec_param in itertools.zip_longest(self.no_sbp_tags_time, sec_params_no_sbp):
            self.results_dict[param_time] = str(datetime.timedelta(seconds=int(sec_param)))
        return self.results_dict
