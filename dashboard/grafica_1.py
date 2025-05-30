import plotly.express as px
import pymysql
import pandas as pd
from dash import html, dcc, callback, Input, Output

def graficar_plotly():
    conexion = pymysql.connect(
        host='localhost',
        user='root',
        password='12345678',
        database='books_db',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    with conexion.cursor() as cursor:
        # Usamos JOIN para obtener el nombre de la categoría
        cursor.execute("""
            SELECT l.*, c.nombre AS categoria
            FROM libros l
            JOIN categorias c ON l.categoria_id = c.id
        """)
        rows = cursor.fetchall()

    conexion.close()

    df = pd.DataFrame(rows)

    # Limpiar y convertir precios
    df["precio"] = df["precio"].str.replace(r"[^\d.]", "", regex=True)
    df = df[df["precio"] != ""]
    df["precio"] = df["precio"].astype(float)

    # Contar libros por categoría
    conteo = df["categoria"].value_counts().reset_index()
    conteo.columns = ["categoria", "count"]

    # Crear gráfico
    fig = px.bar(conteo, x="categoria", y="count",
                 labels={"categoria": "Categoría", "count": "Cantidad"},
                 title="Cantidad de libros por categoría")
    fig.show()