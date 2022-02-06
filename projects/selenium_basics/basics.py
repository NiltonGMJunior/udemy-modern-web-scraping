from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# NOTE: The following won´t work unless "chromedriver" is in your PATH
# from shutil import which
# chrome_path = which("chromedriver")
# driver = webdriver.Chrome(executable_path=chrome_path)

chrome_options = Options()
chrome_options.add_argument("--headless")

# NOTE: Deprecated way of doing it
driver = webdriver.Chrome(executable_path="./chromedriver", options=chrome_options)
driver.get("https://duckduckgo.com")

search_input = driver.find_element(By.ID, "search_form_input_homepage")
search_input.send_keys("My User Agent")

# search_btn = driver.find_element_by_id("search_button_homepage")
# search_btn.click()

search_input.send_keys(Keys.ENTER)

print(driver.page_source)

driver.close()