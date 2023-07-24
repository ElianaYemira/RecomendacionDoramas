import pandas as pd
from bs4 import BeautifulSoup
import requests
import time
from PIL import Image
from io import BytesIO
import json

# Leer el archivo csv
df = pd.read_csv("5000_doramas.csv")

# Añadir una columna url vacía
df["image_url"] = ""

# Para cada fila en el dataframe
for i, row in df.iterrows():
    # Construir la consulta
    query = df.loc[i, "name"] + " drama film"
    url = "https://www.bing.com/images/search?q=" + query

    # Hacer la petición
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Buscar todos los elementos 'a' que tengan el atributo 'm'
    a_tags = soup.find_all("a", {"m": True})

    # Si se encontraron imágenes
    for a_tag in a_tags:
        try:
            # Convertir el valor del atributo 'm' a un diccionario
            img_info = json.loads(a_tag["m"])
            # Guardar la URL de la imagen en la columna 'image_url'
            img_url = img_info.get("murl")

            # Descargar la imagen
            response = requests.get(img_url)
            img = Image.open(BytesIO(response.content))

            # Convertir la imagen a RGB si es RGBA
            if img.mode == "RGBA":
                img = img.convert("RGB")

            # Guardar la imagen
            img.save(f'{i}.jpg')

            # Si la imagen se guardó con éxito, salir del bucle
            print(f"Imagen {i+1} guardada correctamente.")
            df.at[i, "image_url"] = img_url
            break

        except Exception as e:
            # Si hubo un error al descargar la imagen, continuar con la próxima imagen
            print(f"Error al abrir la imagen para el registro {i+1}: {e}")

    # Esperar 3 segundos antes de la siguiente petición
    time.sleep(3)

    # # Si ya hemos procesado 5 filas, salir del bucle
    # if i >= 3:
    #     break

# Guardar el dataframe en un nuevo archivo csv
df.to_csv("5000_DoramasFinal.csv", index=False)
