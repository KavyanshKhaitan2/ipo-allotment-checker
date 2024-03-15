from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
import selenium
import util
import undetected_chromedriver as uc
import os

Str = "Purvashare"

def get_options(driver:uc.Chrome):
	options = []
	driver.get("https://www.purvashare.com/investor-service/ipo-query")
	companyDropDown = Select(driver.find_element("xpath", "//select[@id='company_id']"))
	for i in companyDropDown.options:
		if i.text == "Select Company": continue
		options.append(i.text)
	return options

def get_data(driver:uc.Chrome, options, pans):
	global_results = []
	num = 0
	total = len(options) * len(pans)

	driver.get("https://www.purvashare.com/investor-service/ipo-query")
	for pan, name in pans:
		print(f"Search started for {name}")
		results = []
		for i in options:
			num+=1
			print(f"\nProcessing {i} ({num}/{total})...", end=" ")

			companyDropDown = Select(driver.find_element("xpath", "//select[@id='company_id']"))
			companyDropDown.select_by_visible_text(i)

			panInput = driver.find_element("xpath", "//p[4]/input[@class='form-control']")
			panInput.send_keys(pan)

			submitBtn = driver.find_element("xpath", "//p[5]/input")
			submitBtn.click()

			try:
				if driver.find_element("xpath", "//div[@class='alert alert-warning alert-dismissible fade shadow show']/b"):
					print("No records found: Records set to 0")
					applied = 0
					alloted = 0
					result = [i, applied, alloted]
					results.append(result)
				else: raise(ReferenceError)
				
			except:
				print("Found results")
				applied = driver.find_element("xpath", "//tbody/tr/td[5]").text
				alloted = driver.find_element("xpath", "//tbody/tr/td[6]").text
				result = [i, applied, alloted]
				results.append(result)
			
		global_results.append([name, results])

		print(f"Search complete for {name}")
	return global_results

if __name__ == "__main__":
	driver = uc.Chrome()

	options = get_options(driver)
	pans = util.get_pans()
	data = get_data(driver, options, pans)
	
	new_results = {}
	new_results = util.convert_to_dict(data)

	util.convert_to_json(new_results)

	table = util.convert_to_tabular_list(new_results)
	from tabulate import tabulate
	print(tabulate(table))

	util.convert_to_csv(table, 'purvashare.csv')

	print("All processes executed successfully")