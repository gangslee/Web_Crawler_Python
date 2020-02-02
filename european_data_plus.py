#coding:utf-8
#EUROPEANDATA
import os
import re
import requests
import time
from bs4 import BeautifulSoup

base_url = "https://data.cdc.gov.tw/" # 홈페이지 검색에 기본이 되는 URL
base_file = "C:/Users/LKS/Desktop/taiwan/"
pattern = re.compile( r'\s+' ) # 개행문자 제거를 위한 변수
c_count = 0
# 파싱 함수 정의
def spider( max_page ) :
    page = 1

    while page < max_page :
        url_page = base_url + "en/dataset?page=" + str( page )
        source = requests.get( url_page ) # 페이지 url 파싱
        print(source.text)
        plain_text = source.text
        soup = BeautifulSoup( plain_text , 'lxml') # BueatifulSoup을 통해 정리

        #게시글 관련 작업
        for links in soup.findAll( 'h3' , {'class' : 'dataset-heading'} ) : # 필요한 태그 검색 후 처리
            try :
                link_aTag = links.find( 'a' )
                link_name = link_aTag.text.replace( ' ' , '_' ).replace( '...' , '' ).replace('.','').replace(':','').replace('\\', '').replace('<', '').replace('>', '').replace('/','-').replace('*','').replace('|','').replace('?', '')
                link_source = requests.get( base_url + link_aTag.get('href') )
                plain_text = link_source.text
                link_soup = BeautifulSoup( plain_text , 'lxml')

                folder_count = 0
                        
                for tags in link_soup.findAll('a',{'class' : 'tag-customized'}):
                    if tags.text == ' gender' :
                        folder_count += 1
                        break
                file_base = ''
                if folder_count == 1 : 
                    file_base = base_file+'gender'
                else :
                    file_base = base_file+'etc'
                
                #콘텐츠 관련 작업
                for contents in link_soup.findAll( 'li' , {'class' : 'resource-item'} ) :
                    try :
                        content_aTag = contents.find( 'a' )
                        content_link = base_url+contents.find( 'div' , {'class' : 'btn-group'} ).find('a',{'class' : 'resource-url-analytics'}).get('href')
                        content_title = content_aTag.get('title').replace( ' ' , '_' ).replace(':','').replace('\\', '').replace('<', '').replace('>', '').replace('/','-').replace('*','').replace('|','').replace('?', '')
                        content_format = contents.find( 'span', {'class' : 'format-label'} ).get('data-format')


                        file_path = file_base+'/'+link_name + '/' + content_title + '.' + content_format
                        print (file_path)
                        time.sleep(10)
                        # 폴더만들기
                        if not os.path.exists(file_base+'/'+link_name):
                            os.makedirs(file_base+'/'+link_name)
                            c_count+=1
                            print(1)

                        # 파일 다운로드
                        try :
                            print(content_link)
                            print()
                            content_request = requests.get( content_link , stream = True )
                            with open( file_path , 'wb+' ) as content_file :
                                content_file.write( content_request.content )
                            time.sleep(5)
                                
                        except :
                            print ( link_name + ":"+ content_title + " - download error!" )
                    except :
                        print ( link_name + " - content error!" )
                    
            except :
                print ( page , " - link error!" )
        page = page + 1
        print(page)

     
spider( 12 ) # 함수 실행
print(c_count)
