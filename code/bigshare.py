from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
import selenium
import util
import undetected_chromedriver as uc
import os
import sys
import time

Str = "BigShare"
def get_options(driver:uc.Chrome):
	options = []
	driver.get("https://ipo.bigshareonline.com/IPO_Status.html")
	companyDropDown = Select(driver.find_element("xpath", "//select[@id='ddlCompany']"))
	for i in companyDropDown.options:
		if i.text == "--Select Company--": continue
		options.append(i.text)
	return options


def get_data(driver:uc.Chrome, options, pans):
	global_results = []
	num = 0
	total = len(options) * len(pans)

	driver.get("https://ipo.bigshareonline.com/IPO_Status.html")
	for pan, name in pans:
		print(f"Search started for {name}")
		results = []
		for i in options:
			if i == '--Select Company--': continue
			num+=1
			print(f"\nProcessing {i} ({num}/{total})...", end=" ")

			driver.find_element("xpath", "//body").send_keys(Keys.CONTROL + Keys.HOME)
			companyDropDown = Select(driver.find_element("xpath", "//select[@id='ddlCompany']"))
			companyDropDown.select_by_visible_text(i)
			
			time.sleep(0.1)
			panCheck = Select(driver.find_element("xpath", "//select[@id='ddlSelectionType']"))
			panCheck.select_by_visible_text("PAN Number")

			time.sleep(0.1)

			panInput = driver.find_element("xpath", "//input[@id='txtpan']")
			panInput.clear()
			panInput.send_keys(pan)
			
			time.sleep(0.1)
			while 1:
				captchaInput = driver.find_element("xpath", "//input[@id='captcha-input']")
				captchaInput.click()
				while True:
					value = captchaInput.get_attribute("value")
					if len("" if value is None else value) == 6: 
						break

				submitBtn = driver.find_element("xpath", "//input[@id='btnSearch']")
				submitBtn.click()

				if driver.find_element("xpath", "//label[@id='lblcaptcha']").text == "":
					break

			time.sleep(0.3)
			try:
				if driver.find_element("xpath", "//button[@class='confirm']").is_displayed():
					print("No records found: Records set to 0")
					applied = 0
					alloted = 0
					result = [i, applied, alloted]
					results.append(result)
					driver.find_element("xpath", "//button[@class='confirm']").click()
				else: raise RuntimeError
			except:
				print("Found results")
				applied = driver.find_element("xpath", "//label[@id='lbl4']").text
				alloted = driver.find_element("xpath", "//label[@id='lbl5']").text
				result = [i, applied, alloted]
				results.append(result)
		global_results.append([name, results])
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

	util.convert_to_csv(table, 'bigshare.csv')

	print("All processes executed successfully")