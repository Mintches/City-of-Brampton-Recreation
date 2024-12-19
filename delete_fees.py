from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time, json

# Constants
TEST_ENVIRONMENT = True
FILE_NAME = "delete_fees.csv"
# login based on the environment
if not TEST_ENVIRONMENT:
	LOGIN_URL = "https://cityofbrampton.perfectmind.com/Menu/MemberRegistration/MemberSignIn"
	USERNAME = "[YOUR LOGIN USERNAME]" # replace
	print("!===WARNING: LIVE MODE===!")
else:
	LOGIN_URL = "https://cityofbramptontest.perfectmind.com/Contacts/MemberRegistration/MemberSignIn"
	USERNAME = "bramptontest"
	print("===TEST MODE===")

# Webdriver Initialization
driver = webdriver.Chrome()
driver.implicitly_wait(10)

# Functions
def log_save(file, s):
	# writes string to file and prints to console
	file.write(s + ",") # reformat as needed
	print(s)

def click_js(driver, elem):
	# click element using JavaScript
	driver.execute_script("arguments[0].click();", elem)

# Open website and login
driver.get(LOGIN_URL)
driver.find_element("id", "textBoxUsername").send_keys(USERNAME)

# User-defined range for facility indices
start_idx = int(input("Enter the START value: "))
end_idx = int(input("Enter the END value: "))

# Main loop for processing facilities
while (input("Press ENTER to start/continue or anything else to end: ") == ""):
	curr_idx = start_idx
	with open(FILE_NAME,"w") as file:
		while (curr_idx <= end_idx):
			# attempt click on facility with retries
			for attempt in range(5):
				try:
					time.sleep(1) # wait for any loading
					facilities = driver.find_elements("class name", "k-master-row")
					click_js(driver, facilities[curr_idx])
					break
				except:
					 # retry in case of failure
					print(f"retrying, re-attempt #{attempt + 1}")

			print(f"Processing current facility index: {curr_idx}")
			curr_facility = driver.find_element("class name", "box-tab-caption-active").text
			log_save(file, curr_facility)

			# enter facility edit mode
			edit = driver.find_element("id", "editObject")
			click_js(driver, edit)

			# fetch and parse fee data from JSON
			fee_data_elem = driver.find_element("id","fld_servicedurations")
			fee_data = json.loads(fee_data_elem.get_attribute("value"))
			delete_buttons = driver.find_elements("class name", "pm-plain-button")

			# iterate over fees
			for fee_idx in range(1, len(fee_data)):
				fee_name = fee_data[fee_idx].get("PriceTypeName")
				fee_log = ""
				if any(year in fee_name for year in ["2020", "2021", "2022"]):
					fee_log = "*" # Mark deleted fees with an asterisk (*)
					click_js(driver,delete_buttons[fee_idx])
				fee_log += fee_name
				log_save(file, fee_log)
			file.write("\n")

			# save changes and go back to facility list
			save = driver.find_element("id", "submitLinkVisible")
			click_js(driver, save)
			back = driver.find_element("class name", "back-button-link")
			click_js(driver, back)

			# increment to next facility index
			curr_idx += 1

# finish and close driver window
print("Done!")
driver.close()
