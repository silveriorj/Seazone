import csv
import lxml.html as parser
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

LIST_XPATH = '//div[@id="FMP-target"]'
APTO_XPATH = '//*[@id="FMP-target"]/div/div/div/div'
BASE_URL = 'https://www.vivareal.com.br/venda/santa-catarina/florianopolis/bairros/'


