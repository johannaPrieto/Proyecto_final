import requests
import pandas as pd
import pymysql
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import plotly.express as px
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import time

# --------------------- SCRAPING ---------------------
def obtener_sopa(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, "html.parser")

def extraer_datos_libro(book, base_url):
    title = book.h3.a["title"]
    partial_url = book.h3.a["href"]
    book_url = base_url + "catalogue/" + partial_url.replace("../", "")
    price = book.select_one(".price_color").text.replace("Â", "").strip()
    availability = book.select_one(".availability").text.strip()
    rating_class = book.select_one(".star-rating")["class"]
    rating = rating_class[1] if len(rating_class) > 1 else "Sin calificación"
    soup = obtener_sopa(book_url)
    category = soup.select("ul.breadcrumb li a")[2].text.strip()
    img_url = base_url + soup.select_one(".item img")["src"].replace("../", "")
    return {
        "titulo": title,
        "precio": price,
        "disponibilidad": availability,
        "calificacion": rating,
        "categoria": category,
        "url_imagen": img_url,
        "url_detalle": book_url
    }
def scrapear_libros(base_url, paginas=5):
    libros = []
    next_page = "catalogue/page-1.html"
    actual = 1
    while next_page and actual <= paginas:
        print(f"📘 Scrapeando página {actual}: {base_url}{next_page}")
        soup = obtener_sopa(f"{base_url}{next_page}")
        for libro in soup.select(".product_pod"):
            data = extraer_datos_libro(libro, base_url)
            libros.append(data)
            time.sleep(0.3)
        siguiente = soup.select_one(".next a")
        if siguiente and actual < paginas:
            next_page = "catalogue/" + siguiente["href"]
            actual += 1
        else:
            break
    return libros

# --------------------- MIGRACIÓN MYSQL ---------------------
def migrar_a_mysql(csv_path):
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()

    conexion = pymysql.connect(
        host='localhost',
        user='root',
        password='12345678',
        database='books_db',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = conexion.cursor()

    # Limpiar tablas si existen
    cursor.execute("DROP TABLE IF EXISTS libros")
    cursor.execute("DROP TABLE IF EXISTS categorias")

    # Crear tabla de categorías
    cursor.execute("""
        CREATE TABLE categorias (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) UNIQUE
        )
    """)

    # Crear tabla de libros con FK a categoría
    cursor.execute("""
        CREATE TABLE libros (
            id INT AUTO_INCREMENT PRIMARY KEY,
            titulo TEXT,
            precio VARCHAR(10),
            disponibilidad TEXT,
            calificacion VARCHAR(20),
            url_imagen TEXT,
            url_detalle TEXT,
            categoria_id INT,
            FOREIGN KEY (categoria_id) REFERENCES categorias(id)
        )
    """)

    # Insertar categorías únicas
    categorias_unicas = df["categoria"].dropna().unique()
    categoria_id_map = {}
    for nombre in categorias_unicas:
        cursor.execute("INSERT INTO categorias (nombre) VALUES (%s)", (nombre,))
        categoria_id_map[nombre] = cursor.lastrowid

    # Insertar libros con su categoria_id
    for _, row in df.iterrows():
        categoria = row["categoria"]
        categoria_id = categoria_id_map.get(categoria)
        cursor.execute("""
            INSERT INTO libros (titulo, precio, disponibilidad, calificacion, url_imagen, url_detalle, categoria_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            row["titulo"], row["precio"], row["disponibilidad"], row["calificacion"],
            row["url_imagen"], row["url_detalle"], categoria_id
        ))

    conexion.commit()
    cursor.close()
    conexion.close()
    print("✅ Migración a MySQL con normalización exitosa")

def menu():
    while True:
        print("\n🔸 MENÚ DE OPCIONES 🔸")
        print("1. Scrapear libros y guardar CSV")
        print("2. Migrar datos a MySQL")
        print("3. Mostrar gráfica estática con Plotly")
        print("4. Lanzar dashboard con Dash")
        print("5. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            base_url = "http://books.toscrape.com/"
            libros = scrapear_libros(base_url, paginas=5)
            df = pd.DataFrame(libros)

            # ✅ Limpiar precios: eliminar símbolos y convertir a float
            df["precio"] = df["precio"].str.replace(r"[^\d.]", "", regex=True)
            df["precio"] = pd.to_numeric(df["precio"], errors="coerce")

            df.to_csv("dataset/books_5_paginas.csv", index=False, encoding="utf-8")
            print("📁 CSV guardado correctamente.")

        elif opcion == "2":
            migrar_a_mysql("dataset/books_5_paginas.csv")
        elif opcion == "3":
            graficar_plotly()
        elif opcion == "4":
            lanzar_dash()
        elif opcion == "5":
            print("👋 Hasta luego.")
            break
        else:
            print("❌ Opción inválida. Intenta nuevamente.")

# --------------------- EJECUCIÓN PRINCIPAL ---------------------
if __name__ == "__main__":
    menu()