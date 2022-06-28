from pprint import pprint

with open('.\\studies\\test1\\dest\\2022_06_20\\study1_Done_20220620_165929369552\\Sleep.rep') as f:
    lines = f.readlines()

sleepRepInfo = dict()
GainChangeDict = dict()
PATGainIndexDict = dict()
REDIRGainIndexDict = dict()

GainChange = []
LedCurrentChange = []
TimeStampError = []
count = -1
for line in lines:
    count += 1
    if 'Device' in line:
        Device = lines[count]
        sleepRepInfo["Device"] = Device.split()[2]
    if 'CRC' in line:
        CRC = lines[count]
        sleepRepInfo["CRC"] = CRC
    if 'GainChange' in line:
        GainChange.append(lines[count])
    for i in range(len(GainChange)):
        GainChangeSplit = GainChange[i].split()
        for el in GainChangeSplit:
            match el:
                case 'PAT':
                    PATGainIndexDict.update({"Time=" + GainChangeSplit[2]: "Gain Index=" + GainChangeSplit[5]})
                    PATGainIndexDict.pop("Total=", None)
                    PATGainIndexDict.update({"Total=": len(PATGainIndexDict)})
                    GainChangeDict['PAT'] = PATGainIndexDict
                case 'RED/IR':
                    REDIRGainIndexDict.update({"Time=" + GainChangeSplit[2]: "Gain Index=" + GainChangeSplit[5]})
                    REDIRGainIndexDict.pop("Total=", None)
                    REDIRGainIndexDict.update({"Total=": len(REDIRGainIndexDict)})
                    GainChangeDict['RED/IR'] = REDIRGainIndexDict
    sleepRepInfo['Gain Change'] = GainChangeDict

    if 'LedCurrentChange' in line:
        LedCurrentChange.append(lines[count])
    if 'Error in Time stamp number' in line:
        TimeStampError.append(lines[count])
        sleepRepInfo['Error in Time stamp number'] = len(TimeStampError)

    if 'SBP Sensor type' in line:
        SBP_sensor_type = lines[count]
        sleepRepInfo["SBP Sensor type"] = SBP_sensor_type
    if 'SBP Error' in line:
        SBP_error = lines[count]
        sleepRepInfo["SBP Error"] = SBP_error
    if 'ReSBP type WCP' in line:
        ReSBP_type = lines[count]
        sleepRepInfo["ReSBP type"] = ReSBP_type.split()[2]
#

pprint(GainChange)
print("-" * 30)
pprint(sleepRepInfo)
