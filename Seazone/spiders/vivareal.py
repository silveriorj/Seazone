import csv
import lxml.html as parser
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException


APTO_XPATH = '//div[@data-type="property"]'
BASE_URL = 'https://www.vivareal.com.br/venda/santa-catarina/florianopolis/bairros/'
LINK_URL = '//a[@class="property-card__main-link js-carousel-link"]'

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
        for term in search_list:
            url = BASE_URL + term
            name = term.split('/')[0]
            print('\033[34m'+"[INFO] Extracting the apartments of "+name+"..."+'\033[0;0m')
            self.crawl_url(url)
            image_name = (name) + ".png"
            self.screenshot(image_name, url)

    def crawl_url(self, url):
        print('[INFO] URL:',url)
        self.driver.get(url)
        print('[INFO] Getting aptos...')
        self.get_aptos(160)
        print('[INFO] GOING TOP...')
        self.go_top(url)
        print('[INFO] Parsing...')
        return self.parse_aptos(200)

    def get_aptos(self, num_of_aptos):
        aptos = self.driver.find_elements_by_xpath(APTO_XPATH)
        while True:
            while len(aptos) < num_of_aptos:
                self.next_page()
                aptos.append(self.driver.find_elements_by_xpath(APTO_XPATH))
            break
        return aptos
    
    def next_page(self):
        javaScript = 'document.querySelector("[title="Próxima página"]"));'
        try:
            self.driver.execute_script(javaScript).click()
            return True
        except:
            return False
              
    def go_top(self, url):
        self.driver.get(url)
        self.driver.execute_script(
            "window.scrollTo(0, 0);")

    def screenshot(self, image_name, url):
        self.go_top(url)
        self.driver.save_screenshot('./Images/VivaReal_'+image_name)

    def parse_aptos(self, num):
        ap = len(self.driver.find_elements_by_xpath(APTO_XPATH))
        while True:
            while ap < num:
                html = parser.fromstring(self.driver.page_source)
                aptos = html.xpath(APTO_XPATH)
                ap += len(aptos)
                for apt in aptos:
                    url = apt.xpath('.//*[(@href)]/@href')
                    price = apt.xpath('.//*[(@class="property-card__price js-property-card-prices js-property-card__price-small")]/text()')
                    condo = apt.xpath('.//*[(@class="js-condo-price")]/text()')
                    try:
                        url = url[0]
                    except:
                        url = 'NaN'
                    try:
                        price = price[0]
                        price = price.replace(' ','')
                        price = price.replace('"','')
                        price = price.replace('\n','')
                        price = price.replace('R$', '')
                    except:
                        price = str(0)
                    try:
                        condo = condo[0]
                        condo = condo.replace(' ','')
                        condo = condo.replace('"','')
                        condo = condo.replace('\n','')
                        condo = condo.replace('R$', '')
                    except:
                        condo = str(0)            
                    self.apartment_list.append({
                        "Preço": price,
                        "Condomínio": condo,
                        "URL": url
                    })
                self.next_page()
            break
        return self.apartment_list

    def save_items(self):
        print('[INFO] Saving the apartments...')
        keys = self.apartment_list[0].keys()
        with open("Arquivos/vivareal_aptos.csv", 'w') as f:
            dict_writer = csv.DictWriter(f, keys)
            dict_writer.writeheader()
            dict_writer.writerows(self.apartment_list)