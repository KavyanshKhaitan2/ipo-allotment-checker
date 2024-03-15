from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
import selenium
import undetected_chromedriver as uc
import bigshare, kfintech, linkintime, maashitla, purvashare, skyline
import util

regList = [bigshare, kfintech, linkintime, maashitla, purvashare, skyline]

print("Starting...")

driver = uc.Chrome()
driver.set_window_size(800,1000)
print("Fetching options...")
options = []
for reg in regList:
	options.append([reg.Str, reg.get_options(driver)])


for r_index, registrar in enumerate(options):
	print(f"[{r_index}] {registrar[0]}")
	for i_index, ipo in enumerate(registrar[1]):
		print(f"[{r_index}.{i_index}] {ipo}")
	print()
util.check_console_page(driver)
ids = input("Enter IDs (comma seperated)\n>>> ").split(",")
ipo_ids = []
registrar_ids = []

for id in ids:
	id = id.split(".")
	if len(id) == 1:
		registrar_ids.append(int(id[0]))
	if len(id) == 2:
		ipo_ids.append(id)

reg_to_search = []
for id in registrar_ids:
	for regId, reg in enumerate(regList):
		if regId == id:
			reg_to_search.append(reg)

ipos_to_search = []

for id in ipo_ids:
	for regId, reg in enumerate(regList):
		if regId == int(id[0]):
			ipos_to_search.append([reg, int(id[1])])
print(ipos_to_search)
outputs = []

print("Fetching PAN data...")
pan_data = util.get_pans()

if reg_to_search:
	print("Fetching allotment data [Registrar List] (1/2)...")
	for reg in reg_to_search:
		opt = reg.get_options(driver)
		data = reg.get_data(driver, opt, pan_data)
		new_data = util.convert_to_dict(data)
		print(new_data)
		outputs.append(new_data)

if ipos_to_search:
	print("Fetching allotment data [IPO List] (2/2)...")
	for details in ipos_to_search:
		reg = details[0]
		ipo_index = details[1]
		
		opt = reg.get_options(driver)
		print(opt)
		try:
			opt = [opt[ipo_index]]
		except:
			continue
		data = reg.get_data(driver, opt, pan_data)
		print(data)
		new_data = util.convert_to_dict(data)
		outputs.append(new_data)
		print(new_data)

output = {}

print("Converting to dict...")

def merge_dicts(*dict_args):
    """
    Given any number of dictionaries, shallow copy and merge into a new dict,
    precedence goes to key-value pairs in latter dictionaries.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result

for i in outputs:
	output = merge_dicts(output, i)


print("Converting to tabular list...")
tabular_list = util.convert_to_tabular_list(output)
print(tabular_list)
print("Converting to CSV...")
print(util.convert_to_csv(tabular_list, "output.csv", root=True))

print("Script successfully compelete")
print("Output in 'output.csv'")
exit()