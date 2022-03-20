import time
import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


store_list = {
    'SC00001': '본점',
    'SC00002': '강남점',
    'SC00006': '광주점',
    'SC00011': '김해점',
    'SC00013': '대구점',
    'SC00060': '대전점',
    'SC00005': '마산점',
    'SC00008': '센텀시티점',
    'SC00012': '스타필드하남점',
    'SC00010': '의정부점',
    'SC00009': '천안아산점',
    'SC00003': '타임스퀘어점'
}

store_cd = list(store_list.keys())
datas = []
def scrap(store):

    URL = 'https://www.shinsegae.com/store/floor.do?storeCd='+store
    DRIVER_PATH = '.\chromedriver.exe'

    chrome_options = Options()
    # chrome_options.add_argument( '--headless' )
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument('--disable-logging')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--start-maximized')

    driver = webdriver.Chrome(executable_path=DRIVER_PATH,
                            chrome_options=chrome_options)
    driver.get(URL)

    bld_list = driver.find_elements_by_xpath(
        '//*[@id="FLOOR_LIST"]/div[2]/div[1]/a')   # 건물개수 확인

    for bld in range(1, len(bld_list)+1):

        bld_select = driver.find_element_by_xpath(
            '//*[@id="FLOOR_LIST"]/div[2]/div[1]/a[{}]'.format(bld))
        # driver.execute_script('arguments[0].click();', bld_select)
        bld_select.send_keys(Keys.ENTER)
        time.sleep(3)

        bld_name = bld_select.text

        floor_list = driver.find_elements_by_xpath(
            '//*[@id="FLOOR_LIST"]/div[2]/div[3]/ul/li')

        for floor in range(1, len(floor_list)+1):

            floor_select = driver.find_element_by_xpath(
                '//*[@id="FLOOR_LIST"]/div[2]/div[3]/ul/li[{}]'.format(floor))
            floor_select.click()
            floor_number = floor_select.find_element_by_xpath('a[1]/span[1]').text
            floor_name = floor_select.find_element_by_xpath('a[1]/span[2]').text

            cate_list = driver.find_elements_by_xpath(
                '//*[@id="FLOOR_LIST"]/div[2]/div[3]/div/div[2]/dl')

            for c in range(len(cate_list)):

                cates = cate_list[c].find_element_by_xpath('dt/span')
                cate_name = cates.text
                brands = cate_list[c].find_elements_by_xpath('dd/div/span[1]')

                for idx in range(len(brands)):
                    brand_name = brands[idx].text
                    print('='*50)
                    print('store: {}'.format(store_list[store]))
                    print('building: {}'.format(bld_name))
                    print('floor: {}'.format(floor_number))
                    print('floor_name: {}'.format(floor_name))
                    print('category: {}'.format(cate_name))
                    print('brand: {}'.format(brand_name))

                    # data = {
                    #     "store": store_list[store],
                    #     "building": bld_name,
                    #     "floor": floor_number,
                    #     "floor_name": floor_name,
                    #     "category": cate_name,
                    #     "brand": brand_name
                    #     }

                    datas.append( [
                        store_list[store],
                        bld_name,
                        floor_number,
                        floor_name,
                        cate_name,
                        brand_name] )
                
    return datas

for store in store_cd:
    scrap(store)

## 저장 및 csv 파일
def saveToFile(filename, datas):
    with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerows([['store', 'building', 'floor', 'floor_name', 'category', 'brand']])
        writer.writerows(datas)

saveToFile('./ssg.csv', datas)