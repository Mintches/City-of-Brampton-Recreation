from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

# Constants
TEST_ENVIRONMENT = True
FILE_NAME = "add_fees.csv"
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
	file.write(s + "\n") # reformat as needed
	print(s)

def click_js(driver, elem):
	# click element using JavaScript
	driver.execute_script("arguments[0].click();", elem)

# Open website and login
driver.get(LOGIN_URL)
driver.find_element("id", "textBoxUsername").send_keys(USERNAME)
action = ActionChains(driver)

# Prompt users to define variables
start_idx = int(input("Enter the START value: "))
end_idx = int(input("Enter the END value: "))
fee_name = input("Enter the fee name: ")
fee_amount = input("Enter the fee amount: ")
fee_tax = input("Add tax? (y/n): ") == 'y'
fee_duration = int(input("Enter the fee duration (minutes): "))
fee_online = input("Show online? (y/n): ") == 'y'

# Process current facility list
while (input("Press ENTER to start/continue or anything else to end: ") == ""):
	curr_idx = start_idx
	with open(FILE_NAME,'w') as file:
		while (curr_idx < end_idx):
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

			# enter add fee mode
			add_fee = driver.find_element(By.CSS_SELECTOR, "span[data-field='addserviceduration']")
			click_js(driver, add_fee)

			# search and add fee name
			last_item = driver.find_element(By.CSS_SELECTOR, "#servicedurationselectorwrapper ul li:last-child")
			text_box = last_item.find_element(By.CSS_SELECTOR, "input[placeholder='Search by Name...']")
			text_box.send_keys(fee_name)
			time.sleep(1) # wait for search results to load
			text_box.send_keys(Keys.RETURN)

			# enter fee amount
			amount_box = last_item.find_element(By.CSS_SELECTOR, "span[class='k-widget k-numerictextbox field-web-control']")
			amount_box.click()
			action.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(Keys.DELETE).perform()
			action.send_keys(fee_amount).perform()

			# apply tax if needed
			tax_box = last_item.find_element(By.CSS_SELECTOR, "div.isVisibleShowOnline input.xpl-checkbox")
			if fee_tax:
				tax_box.click()

			# enter fee duration
			date_box = last_item.find_element(By.CSS_SELECTOR, "span[class='minutes-duration-selector']")
			date_box.click()
			action.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(Keys.DELETE).perform()
			action.send_keys(fee_duration).perform()

			# set online status of fee if needed
			online_box = last_item.find_element(By.CSS_SELECTOR, "span.multi-items-online-float input.xpl-checkbox")
			if fee_online:
				online_box.click()
			
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
