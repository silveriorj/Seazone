import csv
import lxml.html as parser
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

APTO_XPATH = '//div[@data-type="property"]'
BASE_URL = 'https://www.vivareal.com.br/aluguel/santa-catarina/florianopolis/bairros/'
LINK_URL = '//a[@class="property-card__main-link js-carousel-link"]'

def new_aptos(driver, min_len):
    return len(driver.find_elements_by_xpath(APTO_XPATH)) > min_len


class VivaRealCrawler(object):

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
        print('[INFO] Getting the Apartment list...')
        for term in search_list:
            url = BASE_URL + term
            self.crawl_url(url)
            image_name = (term.split('/')[0]) + ".png"
            self.screenshot(image_name)

    def crawl_url(self, url):
        self.driver.get(url)
        self.get_aptos(50)
        return self.parse_aptos()

    def get_aptos(self, num_of_aptos):
        print('[INFO] Scrolling down the page...')
        aptos = self.driver.find_elements_by_xpath(APTO_XPATH)
        while len(aptos) < num_of_aptos:
            try:
                WebDriverWait(self.driver, 10).until(
                    lambda driver: new_aptos(driver, len(aptos)))
            except TimeoutException:
                # simple exception handling, just move on in case of Timeout
                aptos = self.driver.find_elements_by_xpath(APTO_XPATH)
                break
            aptos = self.driver.find_elements_by_xpath(APTO_XPATH)
        return aptos

    def go_top(self):
        self.driver.execute_script(
            "window.scrollTo(0, 0);")

    def screenshot(self, image_name):
        self.go_top()
        self.driver.save_screenshot('./Images/VivaReal_'+image_name)

    def parse_aptos(self):
        html = parser.fromstring(self.driver.page_source)
        aptos = html.xpath(APTO_XPATH)
        print('[INFO] Extracting the apartments...')
        for apt in aptos:
            per = apt.xpath('.//*[(@class="property-card__price-period")]/text()')
            url = apt.xpath('.//*[(@href)]/@href')
            price = apt.xpath('.//*[(@class="property-card__price js-property-card-prices js-property-card__price-small")]/text()')
            condo = apt.xpath('.//*[(@class="js-condo-price")]/text()')
            try:
                url = url[0]
                url = url.replace(' ','')
            except:
                url = ''
            try:
                per = per[0]
                per = per.replace(' ','')
                per = per.replace('"','')
                per = per.replace('/','')
                per = per.replace('\n','')
            except:
                per = ''
            try:
                price = price[0]
                price = price.replace(' ','')
                price = price.replace('"','')
                price = price.replace('\n','')
                price = price.replace('R$', '')
            except:
                price = 0
            try:
                condo = condo[0]
                condo = condo.replace(' ','')
                condo = condo.replace('"','')
                condo = condo.replace('\n','')
                condo = condo.replace('R$', '')
            except:
                condo = 0            
            self.apartment_list.append({
                "Preço": price,
                "Condomínio": condo,
                "Período": per,
                "URL": url
            })
        return self.apartment_list

    def save_items(self):
        print('[INFO] Saving the apartments...')
        keys = self.apartment_list[0].keys()
        with open("Arquivos/vivareal_aptos.csv", 'w') as f:
            dict_writer = csv.DictWriter(f, keys)
            dict_writer.writeheader()
            dict_writer.writerows(self.apartment_list)