import csv
import lxml.html as parser
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from threading import Thread,Condition
import time
import random


APTOs_LIST = '//div[@class="_gig1e7"]'
BASE_URL = 'https://www.airbnb.com.br'

def new_aptos(driver, min_len):
    return len(driver.find_elements_by_xpath(APTOs_LIST)) > min_len


class AirbnbCrawl(object):

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1680x1080')
        options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
        self.apartment_list = []

    def crawl_list_and_save(self, search_list):
        print("[INFO] Initializing the crawler...")
        self.crawl_list(search_list)
        self.save_items()
        self.driver.close()

    def crawl_list(self, search_list):
        for term in search_list:
            url = BASE_URL + term
            name = term.split('--')[0]
            name = name.replace("/s/",'')
            print('\033[34m'+"[INFO] Extracting the apartments of "+name+"..."+'\033[0;0m')
            self.crawl_url(url)
            image_name = name + ".png"
            self.screenshot(image_name)

    def crawl_url(self, url):
        print('[INFO] URL:',url)
        self.driver.get(url)
        print('[INFO] Getting aptos...')
        self.get_aptos(160)
        print('[INFO] Parsing... Wait a fell minutes...')
        return self.parse_aptos()

    def get_aptos(self, num_min):
        aptos = self.driver.find_elements_by_xpath(APTOs_LIST)
        while len(aptos) < num_min:
            try:
                self.go_bottom()
                WebDriverWait(self.driver, 10).until(
                    lambda driver: new_aptos(driver, len(aptos)))
            except TimeoutException:
                # simple exception handling, just move on in case of Timeout
                aptos = self.driver.find_elements_by_xpath(APTOs_LIST)
                break
            aptos = self.driver.find_elements_by_xpath(APTOs_LIST)
        print(len(aptos))
        return aptos

    def go_bottom(self):
        self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

    def go_top(self):
        self.driver.execute_script(
            "window.scrollTo(0, 0);")

    def screenshot(self, image_name):
        self.go_top()
        self.driver.save_screenshot('./Images/Airbnbb_'+image_name)

    def parse_aptos(self):
        html = parser.fromstring(self.driver.page_source)
        aptos = html.xpath(APTOs_LIST)
        for apt in aptos:
            url = apt.xpath('.//a[(@class="_15tommw")]/@href')
            try:
                url = url[0]
            except IndexError:
                url = 'NaN'
            gains, price, stars = self.info_apart(url)
            try:
                price = price[0]
                price = price.replace('R$', '')
                price = price.replace('.','')
            except IndexError:
                price = 0 
            try:
                stars = stars[0]
            except IndexError:
                stars = 0
            print(price)
            print(stars)
            self.apartment_list.append({
                "Preço": price,
                "Avaliação": stars,
                "Ganhos 6 Meses": gains,
                "URL": url
            })
        return self.apartment_list

    def info_apart(self,url):
        url = BASE_URL+url
        aluguel = 0
        i, x = 0,0
        self.driver.get(url)
        for i in range(3):
            html = parser.fromstring(self.driver.page_source)
            price = html.xpath('.//span[(@class="_doc79r")]/text()')
            stars = html.xpath('.//div[(@class="_tghtxy2")]/text()')
            tabela = html.xpath('.//div[(@class="_1lds9wb")]')
            for alugado in tabela:
                aluguel += len(alugado.xpath('.//td[(@class="_z39f86g")]'))
            for x in range (2):
                try:
                    WebDriverWait(self.driver, 0.000025).until(
                            lambda driver: self.wait_and_press())
                except ElementClickInterceptedException:
                    WebDriverWait(self.driver, 0.000025).until(
                            lambda driver: self.wait_and_press())
                except TimeoutException:
                    break
        return aluguel, price, stars

    def wait_and_press(self):
        self.driver.find_element_by_xpath('.//*[(@class="_1h5uiygl")]').send_keys('\n')

    def save_items(self):
        print('[INFO] Saving the apartments...')
        keys = self.apartment_list[0].keys()
        with open("Arquivos/airbnb_aptos.csv", 'w') as f:
            dict_writer = csv.DictWriter(f, keys)
            dict_writer.writeheader()
            dict_writer.writerows(self.apartment_list)
