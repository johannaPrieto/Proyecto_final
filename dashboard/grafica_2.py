import pymysql
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import html, dcc

def kpi_libros_layout():
    # Conexión a la base de datos y extracción de datos
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


    print("MUESTRA ORIGINAL:")
    print(df[["precio", "calificacion"]].head(10))

    # LIMPIEZA DE PRECIO
    df["precio"] = df["precio"].astype(str).str.replace(r"[^\d.]", "", regex=True)
    df["precio"] = pd.to_numeric(df["precio"], errors="coerce")


    mapa_calificacion = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }


    df["calificacion"] = df["calificacion"].map(mapa_calificacion)


    print("\nLUEGO DE LIMPIEZA:")
    print(df[["precio", "calificacion"]].dropna().head(10))


    df = df.dropna(subset=["precio", "calificacion"])


    print(f"\nTotal de registros válidos: {len(df)}")


    layout = dbc.Container([
        html.H2("📚 KPI de Libros por Calificación y Precio"),
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H6("Precio Promedio", className="card-title"),
                    html.H4(f"${df['precio'].mean():.2f}", className="card-text")
                ])
            ], style={"backgroundColor": "#2a5674", "color": "white"}), width=4),

            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H6("Calificación Promedio", className="card-title"),
                    html.H4(f"{df['calificacion'].mean():.2f} ★", className="card-text")
                ])
            ], style={"backgroundColor": "#3a718d", "color": "white"}), width=4),

            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H6("Total de Libros", className="card-title"),
                    html.H4(f"{len(df)}", className="card-text")
                ])
            ], style={"backgroundColor": "#2a5674", "color": "white"}), width=4),
        ]),

        html.Br(),
        dbc.Row([
            dbc.Col(
                dcc.Graph(
                    figure=px.scatter(
                        df, x="precio", y="calificacion", color="categoria",
                        hover_data=["titulo"], title="Precio vs Calificación"
                    )
                ), width=6
            ),
            dbc.Col(
                dcc.Graph(
                    figure=px.bar(
                        df.groupby("categoria")["calificacion"].mean().reset_index(),
                        x="categoria", y="calificacion",
                        title="Calificación Promedio por Categoría",
                        labels={"calificacion": "Calificación Promedio", "categoria": "Categoría"},
                        color="calificacion",
                        color_continuous_scale=px.colors.sequential.Blues
                    )
                ), width=6
            )
        ])
    ])

    return layout
