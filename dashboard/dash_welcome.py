from dash import html, Dash

def welcome():
    body = html.Div([

        html.Div([
            html.Div([
                html.Img(
                    src="https://st2.depositphotos.com/1011352/5361/i/450/depositphotos_53614367-stock-photo-inspirational-quote-with-stack-of.jpg",
                    style={"width": "400px", "height": "250px", "marginRight": "30px"}
                ),
            ]),
            html.Div([
                html.H1("The Book", style={"color": "white"}),
                html.P(
                    "Books to Scrape es una página de prueba diseñada para practicar técnicas de web scraping. "
                    "Simula una tienda en línea con libros clasificados por género, precio, calificación y disponibilidad. "
                    "Es ideal para crear dashboards interactivos y desarrollar análisis de datos.",
                    style={"color": "white", "fontSize": "18px"}
                )
            ], style={"flex": "1"})
        ],
        style={
            "backgroundColor": "#2c3e50",
            "height": "50vh",
            "padding": "40px",
            "display": "flex",
            "alignItems": "center"
        }),


        html.Div([
            html.Hr(),
            html.Div([
                html.H1("Encontrarás", style={"color": "#2c3e50"}),
                html.P(
                    "En la página encontrarás una amplia variedad de categorías literarias que se adaptan a todos los gustos y preferencias. Desde géneros clásicos como Ficción, Romance, Misterio y Fantasía, hasta temáticas más específicas como Ficción Cristiana, Autobiografía, Psicología y Negocios. También se incluyen opciones para distintos públicos como Young Adult, New Adult, Infantil y Ficción para Mujeres. Si te interesan los libros de no ficción, podrás explorar categorías como Historia, Ciencia, Salud, Política y Autoayuda. Además, hay espacio para géneros artísticos y creativos como Poesía, Arte, Música y Narrativa Gráfica. Ya sea que busques un clásico literario, un thriller emocionante o una obra espiritual, esta página organiza el contenido en secciones temáticas que facilitan la búsqueda y enriquecen tu experiencia de lectura.",
                    style={"color": "black", "fontSize": "16px"}
                )
            ], style={"marginBottom": "20px"}),
            html.Ul([
                html.Li(
                    html.A("Haz click para visitarnos:)", href="http://books.toscrape.com/index.html", target="_blank")
                )
            ]),
        ],
        style={
            "backgroundColor": "white",
            "height": "50vh",
            "padding": "30px"
        }),
    ],
    style={
        "margin": "0",
        "padding": "0",
        "fontFamily": "Arial, sans-serif"
    })
    return body

if __name__ == "__main__":
    app = Dash(__name__)
    app.layout = welcome()
    app.run(debug=True)
