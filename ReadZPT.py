import numpy as np
import pandas as pd

# convert hexadecimal to decimal
# Create a dtype with the binary data format and the desired column names
try:
    dt = np.dtype('B')
    data = np.fromfile("C:\\Users\\ishir\\PycharmProjects\\sleep-automation\\PatAmplitude.zpt", dtype=dt)
    df = pd.DataFrame(data)
    print(df)
except IOError:
    print("Error while opening the file!")

import numpy as np
dtype = np.dtype('B')
try:
    with open("C:\\Users\\ishir\\PycharmProjects\\sleep-automation\\PatAmplitude.zpt", "rb") as f:
        numpy_data = np.fromfile(f, dtype)
    print(numpy_data)
except IOError:
    print('Error While Opening the file!')

# f = open("C:\\Users\\ishir\\PycharmProjects\\sleep-automation\\PatAmplitude.zpt", "rb")
# import array
# a = array.array("L")  # L is the typecode for uint32
# a.fromfile(f, 3)
# print(a)