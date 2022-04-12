# list of threshold that are not used
## statistics
# case 'RDI':
#     if float(v) > th_dct['RDI']:
#         self.results_dict['RDI'] = [v, 'RDI Problem']
# case 'ODI':
#     if float(v) > th_dct['ODI']:
#         self.results_dict['ODI'] = [v, 'ODI Problem']
# case 'SnoreAbove40':
#     if v == 'W/O SBP':
#         self.results_dict['SnoreAbove40'] = [v]
#     else:
#         h, m, s = self.results_dict['SnoreAbove40'].split(':')          # extracts time from str
#         snore_above_40_sec = int(h) * 3600 + int(m) * 60 + int(s)       # convert to sec
#         if snore_above_40_sec > th_dct['SnoreAbove40']:
#             self.results_dict['SnoreAbove40'] = [v, 'SnoreAbove40 Problem']
# case 'SnoreAbove50':
#     if v == 'W/O SBP':
#         self.results_dict['SnoreAbove50'] = [v]
#     else:
#         h, m, s = self.results_dict['SnoreAbove50'].split(':')          # extracts time from str
#         snore_above_50_sec = int(h) * 3600 + int(m) * 60 + int(s)       # convert to sec
#         if snore_above_50_sec > th_dct['SnoreAbove50']:
#             self.results_dict['SnoreAbove50'] = [v, 'SnoreAbove50 Problem']
# case 'SnoreAbove60':
#     if v == 'W/O SBP':
#         self.results_dict['SnoreAbove60'] = [v]
#     else:
#         h, m, s = self.results_dict['SnoreAbove60'].split(':')          # extracts time from str
#         snore_above_60_sec = int(h) * 3600 + int(m) * 60 + int(s)       # convert to sec
#         if snore_above_60_sec > th_dct['SnoreAbove60']:
#             self.results_dict['SnoreAbove60'] = [v, 'SnoreAbove60 Problem']
# case 'SnoreAbove70':
#     if v == 'W/O SBP':
#         self.results_dict['SnoreAbove70'] = [v]
#     else:
#         h, m, s = self.results_dict['SnoreAbove70'].split(':')          # extracts time from str
#         snore_above_70_sec = int(h) * 3600 + int(m) * 60 + int(s)       # convert to sec
#         if snore_above_70_sec > th_dct['SnoreAbove70']:
#             self.results_dict['SnoreAbove70'] = [v, 'SnoreAbove70 Problem']
# case 'SnoreAbove80':
#     if v == 'W/O SBP':
#         self.results_dict['SnoreAbove80'] = [v]
#     else:
#         h, m, s = self.results_dict['SnoreAbove80'].split(':')          # extracts time from str
#         snore_above_80_sec = int(h) * 3600 + int(m) * 60 + int(s)       # convert to sec
#         if snore_above_80_sec > th_dct['SnoreAbove80']:
#             self.results_dict['SnoreAbove80'] = [v, 'SnoreAbove80 Problem']

## main report
# case 'MeanSatValue':
#     if v == 'N/A':
#         self.results_dict['MeanSatValue'] = [v, 'MeanSatValue is missing']
#     if int(v) > th_dct['MeanSatValue'] + 5 or int(v) < th_dct['MeanSatValue'] - 5:
#         self.results_dict['MeanSatValue'] = [v, 'MeanSatValue Problem']
# case 'MaxSatValue':
#     if v == 'N/A':
#         self.results_dict['MaxSatValue'] = [v, 'MaxSatValue is missing']
#     if int(v) > th_dct['MaxSatValue'] + 5 or int(v) < th_dct['MaxSatValue'] - 5:
#         self.results_dict['MaxSatValue'] = [v, 'MaxSatValue Problem']
# case 'MinSatValue':
#     if v == 'N/A':
#         self.results_dict['MinSatValue'] = [v, 'MinSatValue is missing']
#     if int(v) > th_dct['MinSatValue'] + 5 or int(v) < th_dct['MinSatValue'] - 5:
#         self.results_dict['MinSatValue'] = [v, 'MinSatValue Problem']

## stages
# case 'Sleep[%]':
#     if float(v) > th_dct['Sleep[%]']:
#         self.results_dict['Sleep[%]'] = [v, 'Sleep[%] Problem']
# case 'NREM[%]':
#     if float(v) > th_dct['NREM[%]']:
#         self.results_dict['NREM[%]'] = [v, 'NREM[%] Problem']
# case 'Deep[%]':
#     if float(v) > th_dct['Deep[%]']:
#         self.results_dict['Deep[%]'] = [v, 'Deep[%] Problem']
# case 'Light[%]':
#     if float(v) > th_dct['Light[%]']:
#         self.results_dict['Light[%]'] = [v, 'Light[%] Problem']
