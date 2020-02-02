#coding:utf-8

from selenium import *
from selenium import webdriver
from selenium .webdriver.chrome.options import Options

import bs4
import os
import re
import requests
import time
from bs4 import BeautifulSoup

base_url = "https://data.gov.in" # 홈페이지 검색에 기본이 되는 URL
base_file = "C:/Users/LKS/Desktop/india"

chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : base_file ,"download.prompt_for_download": False,"download.directory_upgrade": True}
chromeOptions.add_experimental_option("prefs", prefs)
driver=webdriver.Chrome('C:\chromedriver.exe',chrome_options=chromeOptions)


pattern = re.compile( r'\s+' ) # 개행문자 제거를 위한 변수
driver.implicitly_wait(5)
def spider() :
    
    c_count = 0
    base_url2 = base_url+'/catalogs'
    base_url3 = base_url+'/catalog'

    page = 3
    max_page = 475
    soup_before=''
    while page < max_page :

        url_page = base_url+'/catalogs#items_per_page=9&page='+str(page)+'&sort_by=created&sort_order=DESC'
        print(url_page)
        page +=1
        driver.get(url_page)
        time.sleep(15)
        soup2 = bs4.BeautifulSoup(driver.page_source,"html.parser")
        while True:
            if soup_before==soup2 :
                time.sleep(15)
                soup2 = bs4.BeautifulSoup(driver.page_source,"html.parser")
            else :
                break
            
        soup_before=soup2
        count = 0
        
        for links in soup2.findAll( 'div' , {'class' : 'ogpl-grid-list'} ) :
            c_count+=1

            if not count == 0 :
            
                try:
                    link_aTag = links.find('span', {'class' : 'field-content'}).find( 'a' )
                    link_name = link_aTag.text.replace( ' ' , '_' ).replace( '...' , '' ).replace('.','').replace(':','').replace('\\', '').replace('<', '').replace('>', '').replace('/','-').replace('*','').replace('|','').replace('?', '')
                    link_categ = links.find('div',{'class' : 'views-field views-field-field-ministry-department'}).find('span').text
                    print(link_name)
                    small_page = 0
                    last_page = links.find('span',{'count-resource'}).text.replace('(','').replace(')','')
                    
                    if not last_page == 'NA' :
                    
                        last_page = int(last_page)//6+1
                                            
                        while small_page < last_page :
                            link_spot = base_url + link_aTag.get('href')+'?title=&file_short_format=&page='+str(small_page)
                            link_source = requests.get(link_spot)
                            plain_text = link_source.text
                            link_soup = BeautifulSoup( plain_text , 'lxml')
                            items_count = 0
                            for items in link_soup.findAll('div', {'class' : 'ogpl-grid-list'}) :

                                if not items_count == 0 :
                                    
                                    try :
                                        content_format = items.find('div', {'class' : 'download-confirmation-box'}).find('div').find('a').text
                                        content_name = items.find('span',{'class' : 'title-content'}).text.replace('"','').replace("'",'').replace(',',' and ').replace( ' ' , '_' ).replace(':',' to ').replace('\\', '').replace('<', '').replace('>', '').replace('/','-').replace('*','').replace('|','').replace('?', '')
                                        content_code = items.find('div',{'class' : 'data-export-cont'}).get('class')[2].replace('confirmationpopup-','')
                                        content_link = 'https://data.gov.in/node/'+content_code+'/download'
                                      
                                        
                                        file_url = base_file+'/'+link_categ+'/'+ link_name
                                        file_path = base_file+'/'+link_categ+'/'+link_name+'/'+content_name+'.'+content_format
                                        
                                        
                                        if not os.path.exists(file_url):
                                            os.makedirs(file_url)
                                        
                            
                                        try :
                                            item_source = requests.get(content_link)
                                            item_text = item_source.text
                                            item_soup = BeautifulSoup( item_text , 'lxml')
                                            item_metaTag  = item_soup.find('meta',{'http-equiv':'refresh'}).get('content').replace('1;url=','')

                                            content_request = requests.get( item_metaTag , stream = True )
                                            with open( file_path , 'wb' ) as content_file :
                                                content_file.write( content_request.content )
                                            time.sleep(5)

                                        except :
                                            print (link_name + ":"+ content_title + " - download error!" )
                                    except :
                                        print (content_name + " - content error!" )

                                items_count+=1
                            print(link_name,'page :',small_page,'complete')

                            small_page+=1

                except :
                    print (link_name + " - link error!" )

            count+=1

        
    print(c_count)
    
spider()

print('finish')
