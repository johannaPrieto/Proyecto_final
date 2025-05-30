import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, callback
from dash_welcome import welcome
from grafica_1 import graficar_plotly


# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Indice", className="display-4"),
        html.Hr(),
        html.P("Objetivo: Mostrar datos", className="lead"),
        dbc.Nav(
            [
                dbc.NavLink("Inicio", href="/", active="exact"),
                dbc.NavLink("Dashboard 1", href="/dash1", active="exact"),
                dbc.NavLink("Dashboard 2", href="/dash2", active="exact"),
                dbc.NavLink("Dashboard 3", href="/dash3", active="exact"),
                dbc.NavLink("GitHub", href="https://github.com/",
                            active="exact", target=""),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)


@callback(Output("page-content", "children"),
              [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return welcome()
    elif pathname == "/dash1":
        return graficar_plotly()
    elif pathname == "/dash":
        return html.P("Oh cool, this is page 3!")
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )


if __name__ == "__main__":
    app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP],
                    suppress_callback_exceptions=True)
    app.layout = html.Div([dcc.Location(id="url"), sidebar, content])
    app.run(debug=True)