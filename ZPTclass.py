import numpy as np
import os


class ZPTclass:
    def __init__(self, zip_folder, subdir, data_mat, zpt_txt):
        self.zip_folder = zip_folder
        self.subdir = subdir
        self.data_mat = data_mat
        self.zpt_txt = zpt_txt
        self.data_mat = self.get_bin_data()

    def get_bin_data(self):
        data_array = np.fromfile(self.zip_folder, dtype=np.int16)
        # The data is presented from byte 128 till the end.
        # Every two bytes represent a value, so we need to start from byte 128/2
        data_array = data_array[64:]
        self.data_mat.append(data_array)
        self.write_zpt_to_txt()
        return self.data_mat

    def write_zpt_to_txt(self):
        study_folder = os.path.join(self.subdir, self.zpt_txt)
        with open(study_folder, 'w') as f:
            for line in self.data_mat:
                f.write(str(line))
                f.write('\n')

