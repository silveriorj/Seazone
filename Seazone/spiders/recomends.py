import pandas as pd
import matplotlib.pyplot as plt

def Reader(url):
   file = pd.read_csv("./Arquivos/"+url+'_aptos.csv')
   print(file)
