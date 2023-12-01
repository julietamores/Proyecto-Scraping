import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import urllib.request
import re

session = requests.Session()

session.get('https://www.elabastecedor.com.ar')         #se agrega esta linea para cargar la página principal y que no genere problemas a la hora de hacer un get de la sigueinte url

url2 = "https://www.elabastecedor.com.ar/verduleria-frutas-perecederas"

web1 = session.get(url2)        #se cambia request por session

soup1 = BeautifulSoup(web1.content, 'html.parser')

# Buscamos los elementos que contienen los productos y precios
productos_BsAs = soup1.find_all('div', class_="nombreProducto")

def BsAs():            
    productosBsAs = list()
    count = 0
    for i in productos_BsAs:
        if count < 17:      #la página sólo cuenta con 17 elementos así que si se busca un número mayor genera problemas
            productosBsAs.append(i.span.text.strip())       #se extrae sólo un campo del div y no todo se texto, en ese caso lo que está contenido dentro de span
        else:
            break
        count += 1

    preciosTotales = soup1.find_all('li', class_='current-price')   #en vez de buscar dentro de un div se busca un 'li'
    precios = list()
    count = 0

    for i in preciosTotales:
        if count < 17:      #de nuevo se busca sólo hasta 17 elementos para evitar conflictos
            precios.append(i.text.strip())          #se extrae el contenido usando strip 
        else:
            break
        count += 1

   
    Pp = pd.DataFrame({"PRODUCTOS": productosBsAs, "PRESENTACION-PRECIOS": precios}, index=list(range(1, 18)))      #se cambia el tamaño nuevamente
    print(Pp)

    Pp.to_csv("ProductosBsAs.csv", index=False)


print("Precios de Verduras en Buenos Aires")
BsAs()


