import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import matplotlib.pyplot as plt
import plotly.express as px

# URL base del sitio
BASE_URL = "http://books.toscrape.com/"


# ----------------------------- FUNCIONES DE SCRAPING -----------------------------

def get_soup(url):
    """Obtiene y parsea el contenido HTML de una URL."""
    response = requests.get(url)
    return BeautifulSoup(response.text, "html.parser")

    
if __name__ == "__main__":
    saludo()
    adios()
