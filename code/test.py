def convert_to_tabular_list(inp):
	table1 = [['Shares Alloted']]
	for name in list(inp.items())[0][1]:
		table1[0].append(name)
	
	for ipo in list(inp.items()):
		line = [ipo[0]]
		for person in list(ipo[1].items()):
			line.append(person[1][1])
		table1.append(line)
	
	table2 = [['Shares Applied']]
	for name in list(inp.items())[0][1]:
		table2[0].append(name)
	
	for ipo in list(inp.items()):
		line = [ipo[0]]
		for person in list(ipo[1].items()):
			line.append(person[1][0])
		table2.append(line)
	return table1+[".","."]+table2
import json

with open("input.json", 'rb') as f:
	data = json.load(f)

table = convert_to_tabular_list(data)

from tabulate import tabulate
print(tabulate(table))