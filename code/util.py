import json
import os
import sys

def get_pans():
	with open("panDB.txt", "r") as f:
		lines = f.readlines()
		print(lines)
		pans = [i.split(",") for i in lines]
		pans = [[no, name.rstrip("\n")] for no, name in pans]
	return pans

def convert_to_json(obj, fileloc = None):
	if fileloc:
		with open(fileloc, "w") as f:
			json.dump(obj, f)
	return json.dumps(obj)

def convert_to_dict(global_results):
	dic = {}
	for account in global_results:
		ipos = account[1]
		for ipo in ipos:
			ipo_name = ipo[0]
			applied = ipo[1]
			alloted = ipo[2]

			name:str = account[0].rstrip("\n")
			try:
				dic[ipo_name][name] = [applied, alloted]
			except KeyError:
				dic[ipo_name] = {}
				dic[ipo_name][name] = [applied, alloted]
	convert_to_json(dic, fileloc="tmp.json")
	return dic

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

def convert_to_csv(input:list, filename:str, root:bool = False):
	table = input
	import csv
	if os.getcwd().endswith("ipo_allotment_chkr"):
		path = "out/"+filename
	else:
		path = "../out/"+filename
	if root:
		path = filename
	while 1:
		try:
			with open(path, 'w', newline='') as f:
				write = csv.writer(f)
				write.writerows(table)
			break
		except Exception as e:
			print("Error:", e)

def check_console_page(driver):
	driver.get(os.path.dirname(os.path.abspath(sys.argv[0])) + "/check_console.html")

if __name__ == "__main__":
	print(os.getcwd())