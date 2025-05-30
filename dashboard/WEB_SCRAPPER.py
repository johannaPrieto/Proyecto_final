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