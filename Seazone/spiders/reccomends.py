import pandas as pd
import matplotlib.pyplot as plt
import lxml.html as parser
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException


options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1680x1080')
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)


BASE_AIR = 'https://www.airbnb.com.br'
BASE_VIVA = 'https://www.vivareal.com.br'


def ReccomendAir(url):
   aptos = pd.read_csv("./Arquivos/"+url+'_aptos.csv')  
   aptos = aptos.sort_values('Avaliação', ascending=False)
   aptos = aptos.head()
   aptos = aptos.sort_values('Preço', ascending=True)
   aptos = aptos.head(3)
   urls = aptos.URL
   ref = 1
   for url in urls:
      image = './Reccomends/Airbnb_'+str(ref)+".png"
      url = BASE_AIR+url
      driver.get(url)
      driver.save_screenshot(image)
      ref+=1

def ReccomendViva(file):
   aptos = pd.read_csv("./Arquivos/"+file+'_aptos.csv')  
   x = aptos.Preço
   y = aptos.Condomínio
   Tendencia(x,y)
   aptos = aptos.sort_values('Condomínio', ascending=True)
   aptos = aptos.head()
   aptos = aptos.sort_values('Preço', ascending=True)
   aptos = aptos.head(3)
   urls = aptos.URL
   
   ref = 1
   for url in urls:
      image = './Reccomends/VivaReal_'+str(ref)+".png"
      url = BASE_VIVA+url
      driver.get(url)
      driver.save_screenshot(image)
      ref+=1
   driver.close()

def Tendencia(x, y):
   plt.plot(x, y)
   plt.savefig('./Tendencia.png', format='png')
