# -*- coding: utf-8 -*-

my_gpu = 'rx 580 8gb'

# imports
from selenium import webdriver
from selenium.webdriver.common.by import By as BY
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from random import randint as RI
#from selenium.common.exceptions import NoSuchElementException
import time

def rw():
    time.sleep(RI(1, 4))
    
# global variables
gvars = {
        'browser': 'chrome'
        , 'url':'https://www.ebay.com/'
        , 'sleep': 10
        , 'implicitwait': 1
        }


chrome_options  = webdriver.ChromeOptions()

# if you wish to use a proxy
# chrome_options.add_argument("--proxy-server=localhost:8081")

# launch chrome and maximize
driver = webdriver.Chrome(options = chrome_options)
driver.maximize_window()

# go to URL
wait = WebDriverWait(driver, gvars['sleep'])
driver.implicitly_wait(gvars['implicitwait'])
driver.get(gvars['url'])

# find and enter zip
rw()
searchbox = wait.until(EC.presence_of_element_located((BY.XPATH, "//input[@class='gh-tb ui-autocomplete-input']")))
searchbox.is_displayed()
searchbox.click()
searchbox.send_keys(my_gpu)
searchbox.send_keys(Keys.RETURN)

# now we need to find completed & sold listings option
soldbox = wait.until(EC.presence_of_element_located((BY.XPATH, "//input[@aria-label='Sold Items']")))
soldbox.click()

# now we are only looking at sold listings

# find big list
biglist  = wait.until(EC.presence_of_element_located((BY.XPATH, "//ul[@class='srp-results srp-list clearfix']")))

# list elements
lels = biglist.find_elements_by_xpath(".//li[@class='s-item s-item__pl-on-bottom']")

# initialize i and place to put things
i = 0
page_results = []


while i < len(lels):
    # current panel
    cp = lels[i]
    
    # initialize as empty
    d = {
         'sold_date': ''
         , 'listing_title': ''
         , 'subtitle': ''
         , 'subsecond': ''
         , 'price': ''
         , 'shipping': ''
         }
    
    # title tag - this contains sold date
    titletag = cp.find_element_by_xpath(".//div[@class='s-item__title--tag']")
    # sold date text
    d['sold_date'] = titletag.find_element_by_xpath(".//span[@class='POSITIVE']").text
    
    # actual listing title
    listingtitle = cp.find_element_by_xpath(".//h3[@class='s-item__title s-item__title--has-tags']")
    d['listing_title'] = listingtitle.text
    
    # all subtitle text - this could be more than just 'preowned/new' so get all
    subtitle = cp.find_element_by_xpath(".//div[@class='s-item__subtitle']")
    d['subtitle'] = subtitle.text
    
    # subtitle secondary - this is just preowned/new
    subsecond = subtitle.find_element_by_xpath(".//span[@class='SECONDARY_INFO']")
    d['subsecond'] = subsecond.text
    
    # item details
    itemdets = cp.find_element_by_xpath(".//div[@class='s-item__details clearfix']")
    
    # price 
    d['price'] = itemdets.find_element_by_xpath(".//span[@class='s-item__price']").text
    
    # shipping
    d['shipping'] = itemdets.find_element_by_xpath(".//span[@class='s-item__shipping s-item__logisticsCost']").text
    
    page_results.append(d)
    i += 1





# quit session and close the webdriver
driver.quit()






















