# Importa las bibliotecas necesarias
import requests  # Para realizar solicitudes HTTP
from bs4 import BeautifulSoup  # Para analizar HTML
import csv  # Para trabajar con archivos CSV
import pandas as pd  # Para manipular y analizar datos
import urllib.request  # Para abrir y leer URL
import re  # Para trabajar con expresiones regulares

# Define las URLs de los sitios web a analizar
url1 = "https://www.abastovirtual.com/productos/verduleria"
url2 = "https://www.elabastecedor.com.ar/verduleria-frutas-perecederas"

# Realiza solicitudes HTTP a las URLs y obtiene las respuestas
web = requests.get(url1)
web1 = requests.get(url2)

# Crea objetos BeautifulSoup para analizar el contenido HTML de las respuestas
soup = BeautifulSoup(web.content, 'html.parser')
soup1 = BeautifulSoup(web1.content, 'html.parser')

# Busca los elementos que contienen los productos y precios en Cordoba
productos_Cba = soup.find_all('div', class_='text')
# Busca los elementos que contienen los productos y precios en BsAs
productos_BsAs = soup1.find_all('div', class_="text")

# Define una función para obtener productos y precios de Cordoba
def Cordoba():
    productosCba = list()
    count = 0
    for i in productos_Cba:
        if count < 17:
            productosCba.append(i.text)
        else:
            break
        count += 1

    # Busca los precios en Cordoba
    preciosCba = soup.find_all('div', class_='product-weight')
    precios = list()
    count = 0
    for i in preciosCba:
        if count < 17:
            precios.append(i.text.replace('\t', '').replace('\n', ''))
        else:
            break
        count += 1

    Pp = pd.DataFrame({"Nombre Producto": productosCba, "Precio Producto Cba": precios}, index=list(range(1, 18)))
    print(Pp)

    # Guarda el DataFrame en un archivo CSV
    Pp.to_csv("ProductosCba.csv", index=False)
    return Pp



# Define una función para obtener productos y precios en BsAs
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

    # Imprime las listas antes de crear el DataFrame
    print("Productos:", productosBsAs)
    print("Precios:", precios)

    Pp = pd.DataFrame({"PRODUCTOS": productosBsAs, "PRESENTACION-PRECIOS": precios}, index=list(range(1, 18)))      #se cambia el tamaño nuevamente
    print(Pp)

    Pp.to_csv("ProductosBsAs.csv", index=False)

BsAs()
           
    


# Define una función para encontrar productos coincidentes entre Cordoba y BsAs
def ProductosCoinciden():
    # Carga los archivos CSV en DataFrames
    df1 = pd.read_csv("ProductosCba.csv")
    df2 = pd.read_csv("ProductosBsAs.csv")

    # Encuentra los nombres de productos que coinciden
    nombres_coinciden = []
    for nombre1 in df1["Nombre Producto"]:
        for nombre2 in df2["Nombre Producto"]:
            if len(set(nombre1.lower()) & set(nombre2.lower())) >= 2:
                nombres_coinciden.append((nombre1, nombre2))
    print(nombres_coinciden)
    
    # Crea un nuevo DataFrame con los resultados
    resultados = pd.DataFrame(columns=["Nombre Producto Cba", "Nombre Producto BsAs", "Precio Cba", "Precio BsAs"])

    for nombre1, nombre2 in nombres_coinciden:
        precio1 = df1.loc[df1["Nombre Producto"] == nombre1, "Precio Producto Cba"].iloc[0]
        precio2 = df2.loc[df2["Nombre Producto"] == nombre2, "Precio Producto BsAs"].iloc[0]
        
        resultados = resultados.append({
            "Nombre Producto Cba": nombre1,
            "Precio Cba": precio1,
            "Nombre Producto BsAs": nombre2,           
            "Precio BsAs": precio2,
        }, ignore_index=True)

    # Guarda el resultado en un nuevo CSV
    resultados.to_csv("Resultado.csv", index=False)



print("Precios de productos en Cordoba")
Cordoba()
print("Precios de productos en BsAs")
BsAs()
ProductosCoinciden()
 
