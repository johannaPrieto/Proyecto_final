import pymysql
import pandas as pd
import plotly.express as px
from dash import html, dcc, Output, Input

def graficar_plotly():
    # Conexión y extracción de datos
    conexion = pymysql.connect(
        host='localhost',
        user='root',
        password='12345678',
        database='books_db',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    with conexion.cursor() as cursor:
        cursor.execute("""
            SELECT l.*, c.nombre AS categoria
            FROM libros l
            JOIN categorias c ON l.categoria_id = c.id
        """)
        rows = cursor.fetchall()
    conexion.close()

    df = pd.DataFrame(rows)
    df["precio"] = df["precio"].astype(str).str.replace(r"[^\d.]", "", regex=True)
    df["precio"] = pd.to_numeric(df["precio"], errors="coerce")
    df = df.dropna(subset=["precio"])

    layout = html.Div([
        html.H2("📚 Cantidad total de libros por categoría"),
        dcc.Graph(id="figLibros")
    ])

    return layout, df

def register_callbacks(app, df):
    @app.callback(
        Output("figLibros", "figure"),
        Input("figLibros", "id")  # Dummy input para que el callback se active al inicio
    )
    def actualizar(_):
        conteo_cat = df.groupby("categoria").size().reset_index(name="Cantidad")
        conteo_cat = conteo_cat.sort_values(by="Cantidad", ascending=False)

        fig = px.bar(
            conteo_cat,
            x="categoria",
            y="Cantidad",
            title="Cantidad total de libros por categoría",
            text="Cantidad",
            color="Cantidad",
            color_continuous_scale=px.colors.sequential.Teal
        )

        fig.update_layout(
            xaxis_title="Categoría",
            yaxis_title="Cantidad de libros",
            xaxis_tickangle=45,
            xaxis_tickfont=dict(size=12),
            yaxis=dict(tickformat="d"),
            width=900,
            height=600,
            margin=dict(t=80, b=150),
            plot_bgcolor="white",
            paper_bgcolor="white"
        )

        fig.update_traces(textposition='outside')

        return fig
 
