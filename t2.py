from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
chromeOptions = Options()
# chromeOptions.headless = True
# chromeOptions.add_argument('--headless')
# chromeOptions.add_argument('--no-sandbox')
# chromeOptions.add_argument('--disable-media-session-api')
prefs={"profile.managed_default_content_settings.images": 2 }
chromeOptions.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(chrome_options=chromeOptions)
driver.get("http://linuxhint.com")
print("Title: %s" % driver.title)
# driver.quit()