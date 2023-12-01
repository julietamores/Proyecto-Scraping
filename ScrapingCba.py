import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import urllib.request


url = "https://www.abastovirtual.com/productos/verduleria"

web = requests.get(url)

soup = BeautifulSoup(web.content, 'html.parser')

productosTotales = soup.find_all('span', class_='text')




def Cordoba():
    productosCba = list()
    count = 0
    for i in productosTotales:
        if count < 17:
            productosCba.append(i.text)
        else:
            break
        count += 1



    preciosTotales = soup.find_all('div', class_='product-weight')
    precios = list()
    count = 0

    for i in preciosTotales:
        if count < 17:
            precios.append(i.text.replace('\t', '').replace('\n', ''))
        else:
            break
        count += 1
   

    Pp = pd.DataFrame({"PRODUCTOS": productosCba, "PRESENTACION-PRECIOS": precios}, index=list(range(1, 18)))
    print(Pp)

    Pp.to_csv("Productos.csv", index=False)
    
print("Precios de Verduras en Cordoba")
Cordoba()