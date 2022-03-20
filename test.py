from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
 
URL = 'http://deal.11st.co.kr/html/nc/deal/main.html'
DRIVER_PATH = '.\chromedriver.exe'

chrome_options = Options()
chrome_options.add_argument( '--headless' )
chrome_options.add_argument( '--log-level=3' )
chrome_options.add_argument( '--disable-logging' )
chrome_options.add_argument( '--no-sandbox' )
chrome_options.add_argument( '--disable-gpu' )

driver = webdriver.Chrome( executable_path=DRIVER_PATH, chrome_options=chrome_options )
driver.get( URL )

datas =list()
elements = driver.find_elements_by_xpath('//*[@id="emergencyPrd"]/div/ul/li')
 
print( '상품 개수: {}'.format( len(elements) ) )
for idx, el in enumerate(elements):
    el_title = el.find_element_by_xpath('div/a/div[3]/p/span[2]')
    el_price = el.find_element_by_xpath('div/a/div[3]/div/span[2]/strong')
 
    tagName = el_title.tag_name
    className = el_title.get_attribute('class')
    title = el_title.text
    price = el_price.text
    
    print( '='*50 )
    print( 'tagName: {}'.format( tagName ) )
    print( 'className: {}'.format( className ) )
    print( 'title: {}'.format( title ) )
    print( 'price: {}'.format( price ) )
    
    data = {
        "no": idx+1
        , "title": title
        , "price": price
    }

    datas.append( data )

print(datas)

