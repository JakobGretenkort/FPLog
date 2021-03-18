import csv
import os
from   selenium.webdriver import Firefox, FirefoxProfile
from   selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from   selenium.webdriver.support.ui import WebDriverWait
import time

WEBSITE_LIST = "website-list.csv"

PROTO = ['http://', 'https://']
PREFIX = ['', 'www.']
PATH = ['/']

BINARY = FirefoxBinary("/home/ba/firefox/obj-x86_64-pc-linux-gnu/dist/bin/firefox")
FP = FirefoxProfile()
FP.set_preference('security.sandbox.content.level', 1)
EXTENSION_PATH = os.path.abspath('extension/')

def try_url(driver, url):
  try:
    driver.get(url)
    time.sleep(5)
    return url
  except:
    return None

def get_driver():
  driver = Firefox(firefox_binary=BINARY, firefox_profile=FP)
  driver.install_addon(EXTENSION_PATH, True)
  driver.set_page_load_timeout(60)
  return driver

def main():

  os.environ['MOZ_DISABLE_CONTENT_SANDBOX'] = '1'

  driver = get_driver()

  with open(WEBSITE_LIST, "r", newline='') as website_list:
    reader = csv.reader(website_list, delimiter=',')

    for column in reader:
      index = int(column[0])
      url = column[1]

      print(index, url, sep=", ")

      url = try_url(driver, url)

      if url is None:
        try:
          driver.close()
        except:
          pass
        driver = get_driver()

      print(url)

  driver.get("about:blank")
  driver.close()

if __name__ == '__main__':
  main()