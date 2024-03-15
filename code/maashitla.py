from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
import selenium
import util
import undetected_chromedriver as uc
import os
import time

Str = "Maashitla"

def get_options(driver:uc.Chrome):
	options = []
	driver.get("https://maashitla.com/allotment-status/public-issues")
	companyDropDown = Select(driver.find_element("xpath", "//select[@id='txtCompany']"))
	for i in companyDropDown.options:
		if i.text == "----Select Company----": continue
		options.append(i.text)
	return options


def get_data(driver:uc.Chrome, options, pans):
	global_results = []
	num = 0
	total = len(options) * len(pans)
	last_details = 0

	driver.get("https://maashitla.com/allotment-status/public-issues")
	for pan, name in pans:
		print(f"Search started for {name}")
		results = []
		for i in options:
			num+=1
			print(f"\nProcessing {i} ({num}/{total})...", end=" ")

			companyDropDown = Select(driver.find_element("xpath", "//select[@id='txtCompany']"))
			companyDropDown.select_by_visible_text(i)


			panInput = driver.find_element("xpath", "//input[@id='txtSearch']")
			panInput.clear()
			panInput.send_keys(pan)

			time.sleep(0.1)

			submitBtn = driver.find_element("xpath", "//input[@id='btnSearch']")
			submitBtn.click()

			start = time.time()
			while 1:
				try:
					elem = driver.find_element("xpath", "//div[@class='contact-form-success alert alert-success mt-4']")
					if elem.text != last_details:
						last_details = elem.text
						break
					if (start+1)<time.time(): break
				except:
					pass
			while 1:
				try:
					details = driver.find_element("xpath", "//div[@class='contact-form-success alert alert-success mt-4']").text
					details = details.split("\n")
					print("Found results")
					applied = details[2].removeprefix("Share Applied: ")
					alloted = details[3].removeprefix("Share Alloted: ")
					result = [i, alloted, applied]
					results.append(result)
					break
				except: pass
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

	util.convert_to_csv(table, 'maashitla.csv')

	print("All processes executed successfully")