import struct
import numpy as np


class ZPTclass(object):
    def __init__(self):
        self.Actigraph = None
        self.PatAmplitude = None
        self.PAT_Infra = None
        self.PeripheralBP = None
        self.HeartRate = None
        self.SaO2 = None
        self.SBP_AC = None
        self.SnoreWP = None
        self.FlatSignals = []
        self.status_zpt = True

    def setZptAtribute(self, pathZpt, name):
        if "Actigraph" in pathZpt:
            self.Actigraph = self.get_bin_data(pathZpt)
            self.check_threshold(self.Actigraph, name)
        elif "PatAmplitude" in pathZpt:
            self.PatAmplitude = self.get_bin_data(pathZpt)
            self.check_threshold(self.PatAmplitude, name)
        elif "PAT_Infra" in pathZpt:
            self.PAT_Infra = self.get_bin_data(pathZpt)
            self.check_threshold(self.PAT_Infra, name)
        elif "PeripheralBP" in pathZpt:
            self.PeripheralBP = self.get_bin_data(pathZpt)
            self.check_threshold(self.PeripheralBP, name)
        elif "HeartRate" in pathZpt:
            self.HeartRate = self.get_bin_data(pathZpt)
            self.check_threshold(self.HeartRate, name)
        elif "SaO2" in pathZpt:
            self.SaO2 = self.get_bin_data(pathZpt)
            self.check_threshold(self.SaO2, name)
        elif "SBP_AC" in pathZpt:
            self.SBP_AC = self.get_bin_data(pathZpt)
            self.check_threshold(self.SBP_AC, name)
        elif "SnoreWP" in pathZpt:
            self.SnoreWP = self.get_bin_data(pathZpt)
            self.check_threshold(self.SnoreWP, name)

    def get_bin_data(self, path):
        """
        this function parses zpt files
        the data is presented from byte 128; every two bytes represent a value, so we start from byte 128/2
        each sample value will be multiplied by 'SampleGain' to get the correct value
        :param path: the path of the zpt file
        :return: array contains the values of the zpt file
        """
        data_array = np.fromfile(path, dtype=np.int16)
        data_array = data_array[64:]
        sample_gain, _ = self.get_sample_rate_gain(path)
        data_array = sample_gain[0] * data_array
        return data_array

    def get_sample_rate_gain(self, path):
        """
        this function extracts sample rate and sample gain from zpt files
        sample rate in samples per second
        :param path: the path of the zpt file
        :return: sample gain
        """
        bytes = []
        with open(path, "rb") as f:
            byte = f.read(4)  # reading 2 bytes each iteration
            while byte:
                bytes.append(byte)
                byte = f.read(4)

        sample_rate_byte = bytes[2]
        sample_gain_byte = bytes[3]

        sample_rate = struct.unpack('<f', sample_rate_byte)
        sample_gain = struct.unpack('<f', sample_gain_byte)
        return sample_gain, sample_rate

    def check_threshold(self, data_array, name):
        flat = np.all(data_array == data_array[0])
        if flat:
            self.FlatSignals.append(name + "signal is flat")
            self.status_zpt = False

