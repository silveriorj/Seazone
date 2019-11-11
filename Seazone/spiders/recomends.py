import pandas as pd
import matplotlib.pyplot as plt
import csv

def ReaderAir(url):
   aptos = pd.read_csv("./Arquivos/"+url+'_aptos.csv')
   aptos.loc['Preço',aptos["Avaliação"]=="NOVO", 'Ganhos', 'URL'] = float(0)    
   # aptos = aptos.sort_values('Avaliação', ascending=False)
   print(aptos.head())
   aptos.to_csv('./Arquivos/airbnb_aptos.csv')