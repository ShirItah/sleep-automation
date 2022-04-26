import numpy as np


class ZPTclass(object):
    def __init__(self):
        self.Actigraph = None
        self.PatAmplitude = None
        self.PAT_Infra = None
        self.PeripheralBP = None
        self.SaO2 = None
        self.zptFile = []

    def setZptAtribute(self, pathZpt):
        if "Actigraph" in pathZpt:
            self.Actigraph = self.get_bin_data(pathZpt)
        elif "PatAmplitude" in pathZpt:
            self.PatAmplitude = self.get_bin_data(pathZpt)
        elif "PAT_Infra" in pathZpt:
            self.PAT_Infra = self.get_bin_data(pathZpt)
        elif "PeripheralBP" in pathZpt:
            self.PeripheralBP = self.get_bin_data(pathZpt)
        elif "SaO2" in pathZpt:
            self.SaO2 = self.get_bin_data(pathZpt)
        self.zptFile.append(pathZpt)

    @classmethod
    def get_bin_data(cls, path):
        """
        this function parses zpt files (convert binary data to numpy array)
        the data is presented from byte 128; every two bytes represent a value, so we start from byte 128/2
        :param path: the path of the zpt file
        :return: array contains the values of the zpt file
        """
        data_array = np.fromfile(path, dtype=np.int16)
        data_array = data_array[64:]
        return data_array

    def zpt_to_dict(self):
        return self.__dict__
