import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
 
URL = 'https://www.shinsegae.com/store/floor.do?storeCd=SC00001'
DRIVER_PATH = '.\chromedriver.exe'

chrome_options = Options()
# chrome_options.add_argument( '--headless' )
chrome_options.add_argument( '--log-level=3' )
chrome_options.add_argument( '--disable-logging' )
chrome_options.add_argument( '--no-sandbox' )
chrome_options.add_argument( '--disable-gpu' )

driver = webdriver.Chrome( executable_path=DRIVER_PATH, chrome_options=chrome_options )
driver.get( URL )

datas = list()
ssg_list = pd.DataFrame()

bld_list = driver.find_elements_by_xpath('//*[@id="FLOOR_LIST"]/div[2]/div[1]/a')   # 건물개수 확인

for bld in range(1, len(bld_list)+1):    

    bld_select = driver.find_element_by_xpath('//*[@id="FLOOR_LIST"]/div[2]/div[1]/a[{}]'.format(bld))
    bld_select.send_keys(Keys.ENTER)
    time.sleep(3)

    bld_name = bld_select.text

    floor_list = driver.find_elements_by_xpath('//*[@id="FLOOR_LIST"]/div[2]/div[3]/ul/li')
    
    
    for floor in range(1, len(floor_list)+1):

        floor_select = driver.find_element_by_xpath('//*[@id="FLOOR_LIST"]/div[2]/div[3]/ul/li[{}]'.format(floor))
        floor_select.click()
        floor_number = floor_select.find_element_by_xpath('a[1]/span[1]').text
        floor_name = floor_select.find_element_by_xpath('a[1]/span[2]').text

        cate_list = driver.find_elements_by_xpath('//*[@id="FLOOR_LIST"]/div[2]/div[3]/div/div[2]/dl')


        for c in range(len(cate_list)):
            
            cates = cate_list[c].find_element_by_xpath('dt/span')
            cate_name = cates.text
            brands = cate_list[c].find_elements_by_xpath('dd/div/span[1]')


            for idx in range(len(brands)):
                brand_name = brands[idx].text
                print( '='*50 )
                print('building: {}'.format(bld_name))
                print('floor: {}'.format(floor_number))
                print('floor_name: {}'.format(floor_name))
                print('category: {}'.format(cate_name))
                print('brand: {}'.format(brand_name))
                
                # ssg_list['building'] = bld_name
                # ssg_list['floor'] = floor_number
                # ssg_list['floor_name'] = floor_name
                # ssg_list['category'] = cate_name
                # ssg_list['brand'] = brand_name
                # ssg_list.to_csv('./ssg.csv', encoding='utf-8')
                data = {
                    "building": bld_name,
                    "floor": floor_number,
                    "floor_name": floor_name,
                    "category": cate_name,
                    "brand": brand_name
                    }

                datas.append( data )

print(datas)

