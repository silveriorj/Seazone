import csv
import lxml.html as parser
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

LIST_XPATH = ''
APTO_XPATH = '//div[@data-type="property"]'
BASE_URL = 'https://www.vivareal.com.br/venda/santa-catarina/florianopolis/bairros/'

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
            image_name = (term.split('~')[0]) + ".png"
            self.screenshot(image_name)

    def crawl_url(self, url):
        self.driver.get(url)
        self.get_aptos(150)
        return self.parse_aptos()

    def get_aptos(self, num_of_aptos):
        print('[INFO] Scrolling down the page...')
        aptos = self.driver.find_elements_by_xpath(APTO_XPATH)
        while len(aptos) < num_of_aptos:
            try:
                self.go_bottom()
                WebDriverWait(self.driver, 10).until(
                    lambda driver: new_aptos(driver, len(aptos)))
            except TimeoutException:
                # simple exception handling, just move on in case of Timeout
                aptos = self.driver.find_elements_by_xpath(APTO_XPATH)
                break
            aptos = self.driver.find_elements_by_xpath(APTO_XPATH)
        return aptos

    def go_bottom(self):
        self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

    def go_top(self):
        self.driver.execute_script(
            "window.scrollTo(0, 0);")

    def screenshot(self, image_name):
        self.go_top()
        self.driver.save_screenshot('VivaReal_'+image_name)

    def parse_aptos(self):
        html = parser.fromstring(self.driver.page_source)
        aptos = html.xpath(APTO_XPATH)
        print('[INFO] Extracting the apartments...')
        for apt in aptos:
            ad = apt.xpath(
                ".//*[(@class='_1dss1omb')]/text()")
            price = apt.xpath(
                ".//*[(@class='_1jlnvra2')]/descendant-or-self::*"
                "/text()")
            try:
                stars = apt.xpath(
                    ".//*[(@class='_tghtxy2')]"
                    "/descendant-or-self::*/text()")
            except IndexError:
                stars = "NOVO"
            self.apartment_list.append({
                "Anúncio": ad,
                "Preço": price,
                "Avaliação": stars
            })
        return self.apartment_list

    def save_items(self):
        print('[INFO] Saving the apartments...')
        keys = self.apartment_list[0].keys()
        with open("Arquivos/vivareal_aptos.csv", 'w') as f:
            dict_writer = csv.DictWriter(f, keys)
            dict_writer.writeheader()
            dict_writer.writerows(self.apartment_list)