#coding:utf-8
#EUROPEANDATA
import os
import re
import requests
import time
from bs4 import BeautifulSoup

base_url = "https://data.gov.tw/en" # 홈페이지 검색에 기본이 되는 URL
base_file = "C:/Users/LKS/Desktop/taiwan/"
pattern = re.compile( r'\s+' ) # 개행문자 제거를 위한 변수
c_count = 0
total_pages = [24, 4, 38, 13, 32, 33, 1, 104, 54, 114, 56, 37, 3, 155, 1, 14, 5, 1733]

# 파싱 함수 정의
def spider() :
    
    source = requests.get( base_url) # 페이지 url 파싱
    plain_text = source.text
    soup = BeautifulSoup( plain_text , 'lxml') # BueatifulSoup을 통해 정리
    categ_count=0
    for category in soup.findAll('div',{'class' : 'inner-wrapper'}) :
        categ_count+=1
        if categ_count>9 :
            categ_title = category.find('a').text
            category = category.find('a').get('href')
            print(categ_title)
            for max_page in total_pages :
                page = 0
                while page < max_page :
            
                    url_page = base_url + category + '&page='+str( page )
                    url_page=url_page.replace('/en','')
                    print(url_page)

                    source = requests.get( url_page ) # 페이지 url 파싱
                    plain_text = source.text
                    soup = BeautifulSoup( plain_text , 'lxml')

                    for links in soup.findAll( 'header' , {'class' : 'node-header'} ) : # 필요한 태그 검색 후 처리
                        try :
                            
                            link_aTag = links.find( 'a' )
                            link_name = link_aTag.text.replace( ' ' , '_' ).replace( '...' , '' ).replace('.','').replace(':','').replace('\\', '').replace('<', '').replace('>', '').replace('/','-').replace('*','').replace('|','').replace('?', '')
                            link_source = requests.get( base_url + link_aTag.get('href') )
                            plain_text = link_source.text
                            link_soup = BeautifulSoup( plain_text , 'lxml')

                            for contents in link_soup.findAll( 'div' , {'class' : 'field-item'} ) :
                                try :
                                    content_spanTag = contents.find('span',{'class' : 'ff-desc'})
                                    print('여기까지')
                                    print(content_spanTag.text)
                                    content_link = contents.find('a',{'class' : 'dgresource'}).get('href')
                                    content_title = content_spanTag.text.replace( ' ' , '_' ).replace(':','').replace('\\', '').replace('<', '').replace('>', '').replace('/','-').replace('*','').replace('|','').replace('?', '')
                                    content_format = contents.find( 'a', {'class' : 'dgresource'} ).text

                                    file_path = base_file+'/'+link_name + '/' + content_title + '.' + content_format

                                    if not os.path.exists(file_base+'/'+link_name):
                                        os.makedirs(file_base+'/'+link_name)
                                        c_count+=1
                                        

                                    try :
                                        print(content_link)
                                        print()
                                        content_request = requests.get( content_link , stream = True )
                                        with open( file_path , 'wb+' ) as content_file :
                                            content_file.write( content_request.content )
                                        time.sleep(7)
                                    
                                    except :
                                        print ( link_name + ":"+ content_title + " - download error!" )
                                except :
                                    #print ( link_name + " - content error!" )
                                    print ( " - content error!" )
                        except :
                            print ( page , " - link error!" )
                    page = page + 1
                    print(page)

        
     
spider() # 함수 실행
print(c_count)
