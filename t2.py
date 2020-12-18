from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
chromeOptions = Options()
chromeOptions.headless = True
browser = webdriver.Chrome(options=chromeOptions)
browser.get("http://linuxhint.com")
print("Title: %s" % browser.title)
browser.quit()