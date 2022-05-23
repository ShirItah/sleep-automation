# Read a binary file into a byte array
# The format is little-endian
import numpy as np
import struct

Bytes = []  # creating an empty list for the bytes in the file
BytesHex = []  # creating an empty list for the corresponding hexadecimal string
DataList = []  # creating an empty list for the final values
FileName = "SBP_AC.zpt"


def main():
    """
    Main function
    """
    get_bin_data(Bytes, BytesHex, DataList, FileName)


def get_bin_data(bytes, byteshex, datalist, filename):
    with open(".\\" + filename, "rb") as f:
        byte = f.read(4)  # reading 2 bytes each iteration
        while byte:
            bytes.append(byte)
            byte = f.read(4)

    # The data is presented from byte 128 till the end.
    # Every two bytes represent a value, so we need to start from byte 128/2
    # bytes = bytes[:64]
    print(bytes)
    sample_rate_byte = bytes[2]
    sample_gain_byte = bytes[3]

    sample_rate = struct.unpack('<f', sample_rate_byte)
    sample_gain = struct.unpack('<f', sample_gain_byte)
    print(sample_rate, sample_gain)
    print(sample_rate[0]*sample_gain[0])

    # print(bytes)
    # print(struct.unpack('<f', bytes[2]))
    # print(struct.unpack('<f', bytes[3]))
    # Convert an integer number (in bytes list) to the corresponding hexadecimal string
    for bt in bytes:
        byteshex.append(bt.hex())
    # print(byteshex)

    # Convert a little-endian hexadecimal string to a big-endian
    # Afterward, convert the hexadecimal value back to string and convert it to an integer

    for little_endian in byteshex:
        big_endian = little2big(little_endian)
        datalist.append(int(big_endian, 16))
    # print("data list:", datalist)


def little2big(val):
    big_hex = bytearray.fromhex(val)
    big_hex.reverse()
    big_str = ''.join(format(x, '02x') for x in big_hex)
    return big_str


if __name__ == '__main__':
    main()
