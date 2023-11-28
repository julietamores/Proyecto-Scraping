import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import urllib.request
import re

url2 = "https://www.elabastecedor.com.ar/verduleria-frutas-perecederas"
web1 = requests.get(url2)
soup1 = BeautifulSoup(web1.content, 'html.parser')

# Buscamos los elementos que contienen los productos y precios
productos_BsAs = soup1.find_all('div', class_="nombreProducto")

def BsAs():            
    productosBsAs = list()
    count = 0
    for i in productos_BsAs:
        if count < 26:
            productosBsAs.append(i.text)
        else:
            break
        count += 1

    preciosTotales = soup1.find_all('div', class_="product-link")
    precios = list()
    count = 0

    for i in preciosTotales:
        if count < 25:
            precios.append(i.text.replace('\t', '').replace('\n', ''))
        else:
            break
        count += 1

    # Imprime las listas antes de crear el DataFrame
    print("Productos:", productosBsAs)
    print("Precios:", precios)

    Pp = pd.DataFrame({"PRODUCTOS": productosBsAs, "PRESENTACION-PRECIOS": precios}, index=list(range(1, 26)))
    print(Pp)

    Pp.to_csv("ProductosBsAs.csv", index=False)

BsAs()
