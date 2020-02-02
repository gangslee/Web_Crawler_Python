import bs4
from selenium import *
from selenium import webdriver
from selenium .webdriver.chrome.options import Options

import time
import os
import re
import requests
import sys

index = 0
page = 1
max_page = 2


#크롬 옵션 설정 함수
def give_chrome_option(folder_path):
    chromeOptions = webdriver.ChromeOptions()
    prefs = {"download.default_directory" : folder_path,
           "download.prompt_for_download": False,
           "download.directory_upgrade": True}
    chromeOptions.add_experimental_option("prefs", prefs)
    return chromeOptions


chromeOptions = webdriver.ChromeOptions()
file_path = "C:/Users/LKS/Desktop/taiwan/"
prefs = {"download.default_directory" : file_path,"download.prompt_for_download": False,"download.directory_upgrade": True}
chromeOptions.add_experimental_option("prefs", prefs)
driver=webdriver.Chrome('C:\chromedriver.exe',chrome_options=chromeOptions)

while page < max_page :
    print(page)
    base_url = "https://data.cdc.gov.tw/"
    url = base_url + "en/dataset?page=" + str(page)

    driver.get(url)
    soup = bs4.BeautifulSoup(driver.page_source,"html.parser")

    for links in soup.findAll( 'h3' , {'class' : 'dataset-heading'} ) :
        main_link = links.find('a')
        try :
            driver.get(base_url + main_link.get('href') )
            
            lists = driver.find_element_by_xpath('//ul[@class="resource-list"]')
            
            drops = lists.find_elements_by_class_name('resource-item')
            
            time.sleep(3)
            i=0
            for item in drops :
                print(i)
                item.find_element_by_xpath('//a[@class="btn btn-primary dropdown-toggle"]').click()
                time.sleep(5)
                content = item.find_element_by_xpath('//a[@class="resource-url-analytics"]/href')
                print(content.text)
                item.find_element_by_xpath('//a[@class="resource-url-analytics"]').click()
                time.sleep(5)
                i+=1

            '''
            for items in soup2.findAll('div',{'class' : 'dropdown btn-group'}):
                items.find_element_by_xpath('//a[@class="btn btn-primary dropdown-toggle"]').click()
                items.find_element_by_xpath('//a[@class="resource-url-analytics"]').click()
                time.sleep(5)
            '''
           
            
            
            
        except :
            print (" - link error!" )
            


    page+=1
