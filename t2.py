from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
chromeOptions = Options()
chromeOptions.headless = True
chromeOptions.add_argument('--headless')
chromeOptions.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=chromeOptions)
driver.get("http://linuxhint.com")
print("Title: %s" % driver.title)
driver.quit()