import platform
import sys
from selenium import webdriver, common


def get_headless_chrome():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    print('get CHROME HEADLESS')
    try:
        if platform.system() == 'Windows':
            return webdriver.Chrome(sys.path[0] + '\superform\selenium_drivers\chromedriver.exe', chrome_options=options)
        else:
            return webdriver.Chrome(sys.path[0] + '/superform/selenium_drivers/chromedriver', chrome_options=options)
    except common.exceptions.WebDriverException:
        sys.exit('Can not find a valid chrome driver. it should be named chromedriver on linux or chromedriver.exe '
                 'on windows and it should be located in the superform/selenium_drivers folder see this page for '
                 'download : https://sites.google.com/a/chromium.org/chromedriver/downloads')


def get_chrome():
    try:
        if platform.system() == 'Windows':
            return webdriver.Chrome(sys.path[0] + '\superform\selenium_drivers\chromedriver.exe')
        else:
            return webdriver.Chrome(sys.path[0] + '/superform/selenium_drivers/chromedriver')
    except common.exceptions.WebDriverException:
        sys.exit('Can not find a valid chrome driver. it should be named chromedriver on linux or chromedriver.exe '
                 'on windows and it should be located in the superform/selenium_drivers folder see this page for '
                 'download : https://sites.google.com/a/chromium.org/chromedriver/downloads')