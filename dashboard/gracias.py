import dash
from dash import html, dcc

def pagina_gracias():
    return html.Div(
        style={
            "display": "flex",
            "flexDirection": "column",
            "alignItems": "center",
            "justifyContent": "center",
            "height": "100vh",
            "backgroundColor": "#f0f8ff",
        },
        children=[
            html.H1("¡Gracias!", style={
                "fontSize": "64px",
                "color": "#2a5674",
                "marginBottom": "30px",
                "textShadow": "2px 2px 5px #3a718d"
            }),
            html.Img(
                src="https://i.pinimg.com/originals/1f/0b/85/1f0b85bb750807778b1fe2444527fbd2.gif",
                style={
                    "width": "600px",
                    "borderRadius": "15px",
                    "boxShadow": "0 0 15px rgba(0,0,0,0.2)"
                }
            )
        ]
    )


if __name__ == "__main__":
    app = dash.Dash(__name__)
    app.layout = pagina_gracias()
    app.run_server(debug=True)
