# Read a binary file into a byte array
# The format is little-endian
import numpy as np

Bytes = []  # creating an empty list for the bytes in the file
BytesHex = []  # creating an empty list for the corresponding hexadecimal string
DataList = []  # creating an empty list for the final values
FileName = "PatAmplitude.zpt"


def main():
    """
    Main function
    """
    get_bin_data(Bytes, BytesHex, DataList, FileName)


def get_bin_data(bytes, byteshex, datalist, filename):
    # f = open(".\\" + filename, "rb")
    # byte = f.read(2)  # reading 2 bytes each iteration
    # while byte:
    #     bytes.append(byte)
    #     byte = f.read(2)
    with open(".\\" + filename, "rb") as f:
        byte = f.read(2)  # reading 2 bytes each iteration
        while byte:
            bytes.append(byte)
            byte = f.read(2)
    # The data is presented from byte 128 till the end.
    # Every two bytes represent a value, so we need to start from byte 128/2
    bytes = bytes[64:]
    # print(bytes)

    # Convert an integer number (in bytes list) to the corresponding hexadecimal string
    for bt in bytes:
        byteshex.append(bt.hex())
    # print(byteshex)

    # Convert a little-endian hexadecimal string to a big-endian
    # Afterward, convert the hexadecimal value back to string and convert it to an integer

    for little_endian in byteshex:
        big_endian = little2big(little_endian)
        datalist.append(int(big_endian, 16))
    print(datalist)


def little2big(val):
    big_hex = bytearray.fromhex(val)
    big_hex.reverse()
    big_str = ''.join(format(x, '02x') for x in big_hex)
    return big_str


if __name__ == '__main__':
    main()
