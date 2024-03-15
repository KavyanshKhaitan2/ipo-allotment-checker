from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
import selenium
import util
import undetected_chromedriver as uc
import os
import sys
import time

Str = "KFinTech"
def get_options(driver:uc.Chrome):
	options = []
	driver.get("https://rti.kfintech.com/ipostatus/")
	companyDropDown = Select(driver.find_element("xpath", "//select[@id='ddl_ipo']"))
	for i in companyDropDown.options:
		if i.text == "--Select--": continue
		options.append(i.text)
	return options

def get_data(driver:uc.Chrome, options, pans):
	global_results = []
	num = 0
	total = len(options) * len(pans)

	driver.get("https://rti.kfintech.com/ipostatus/")
	for pan, name in pans:
		print(f"Search started for {name}")
		results = []
		for i in options:
			if i == '--Select--': continue
			num+=1
			print(f"\nProcessing {i} ({num}/{total})...", end=" ")

			companyDropDown = Select(driver.find_element("xpath", "//select[@id='ddl_ipo']"))
			companyDropDown.select_by_visible_text(i)
			
			panCheck = driver.find_element("xpath", "//input[@id='pan']")
			panCheck.click()

			while 1:
				try:
					panInput = driver.find_element("xpath", "//input[@id='txt_pan']")
					panInput.clear()
					panInput.send_keys(pan)
					break
				except: pass

			captchaInput = driver.find_element("xpath", "//input[@id='txt_captcha']")
			captchaInput.click()
			while True:
				value = captchaInput.get_attribute("value")
				print(value)
				if len("" if value is None else value) == 6: 
					break

			submitBtn = driver.find_element("xpath", "//a[@id='btn_submit_query']")
			submitBtn.click()

			try:
				if driver.find_element("xpath", "//button[@class='btn btn-blue']").is_displayed():
					print("No records found: Records set to 0")
					applied = 0
					alloted = 0
					result = [i, applied, alloted]
					results.append(result)
					driver.find_element("xpath", "//button[@class='btn btn-blue']").click()
				else: raise RuntimeError
			except:
				print("Found results")
				applied = driver.find_element("xpath", "//span[@id='grid_results_ctl02_Label5']").text
				alloted = driver.find_element("xpath", "//span[@id='grid_results_ctl02_lbl_allot']").text
				result = [i, applied, alloted]
				results.append(result)
				driver.find_element("xpath", "//a[@id='lnk_new']").click()
		global_results.append([name, results])

		print(f"Search complete for {name}")
	return global_results


if __name__ == "__main__":
	driver = uc.Chrome()

	pans = util.get_pans()
	options = get_options(driver)

	driver.get(os.path.dirname(os.path.abspath(sys.argv[0])) + "/check_console.html")
	for i, item in enumerate(options): print(f"[{i}] {item}")
	index = int(input("\nEnter index for the IPO allotment to be checked for\n>>> "))
	options = [options[index]]

	data = get_data(driver, options, pans)

	new_results = {}
	new_results = util.convert_to_dict(data)

	util.convert_to_json(new_results)

	table = util.convert_to_tabular_list(new_results)
	from tabulate import tabulate
	print(tabulate(table))

	util.convert_to_csv(table, 'kfintech.csv')

	print("All processes executed successfully")