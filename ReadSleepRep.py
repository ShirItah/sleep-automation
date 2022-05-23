from pprint import pprint
with open('.\\studies\\results\\study1\\Sleep.rep') as f:
    lines = f.readlines()

# pprint(lines)

with open('.\\studies\\results\\study1\\zpt_data.txt') as f:
    lines = f.readlines()
pprint(lines)
print(lines[0])
print(type(lines[0]))
print(len(lines[0]))