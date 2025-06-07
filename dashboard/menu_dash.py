import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, callback
from dash_welcome import welcome
from grafica_1 import graficar_plotly, register_callbacks
from grafica_2 import kpi_libros_layout



# Estilos
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}


sidebar = html.Div([
    html.H2("Indice", className="display-4"),
    html.Hr(),
    html.P("Datos destacados", className="lead"),
    dbc.Nav([
        dbc.NavLink("Inicio", href="/", active="exact"),
        dbc.NavLink("Categoria", href="/dash1", active="exact"),
        dbc.NavLink("Calificacion", href="/dash2", active="exact"),
        dbc.NavLink("¡Gracias!", href="/dash3", active="exact"),
        dbc.NavLink("eBook", href="https://books.toscrape.com/index.html", active="exact", target="_blank"),
    ], vertical=True, pills=True),
], style=SIDEBAR_STYLE)

content = html.Div(id="page-content", style=CONTENT_STYLE)


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)


graf_layout, df_libros = graficar_plotly()


register_callbacks(app, df_libros)

# Routing
@callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return welcome()
    elif pathname == "/dash1":
        return graf_layout
    elif pathname == "/dash2":
        return kpi_libros_layout()
    elif pathname == "/dash3":
        return html.P("Dashboard 3 en construcción.")
    return html.Div([
        html.H1("404: Página no encontrada", className="text-danger"),
        html.Hr(),
        html.P(f"La ruta {pathname} no fue reconocida.")
    ], className="p-3 bg-light rounded-3")


app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])


if __name__ == "__main__":
    app.run(debug=True)
