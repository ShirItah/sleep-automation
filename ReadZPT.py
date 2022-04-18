# Read a binary file into a byte array
# The format is little-endian
import numpy as np

FileName = "PatAmplitude.zpt"


def main():
    """
    Main function
    """
    get_bin_data(FileName)


def get_bin_data(filename):
    with open(".\\" + filename, "rb") as f:
        data_array = np.fromfile(f, dtype=np.int16)
        # The data is presented from byte 128 till the end.
        # Every two bytes represent a value, so we need to start from byte 128/2
        data_array = data_array[64:]
        print(data_array)
    # data_array = np.fromfile(".\\" + filename, dtype=np.int16)
    # data_array = data_array[64:]
    # print(data_array)

if __name__ == '__main__':
    main()
