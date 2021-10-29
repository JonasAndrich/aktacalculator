import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from datetime import datetime, timedelta

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

server = app.server

app.layout = html.Div([
    html.H1("ÄKTA Flow Calculator"),
    html.H3("Wann kommst Du morgen zur ÄKTA?"),
    html.Label([
        dcc.Input(id='h', type='number', min=0, max=24, step=1, value=8),
        "Uhr und ",
        dcc.Input(id='m', type='number', min=0, max=59, step=1, value=0),
        "Minuten", ]),

    html.H3("Wie viel Volumen Lysat ist in der Flasche?"),
    html.Label([dcc.Input(id='volume', type='number', min=50, max=10000, step=1, value=1000), "mL"]),

    html.H3("Wie viel Flüssigkeit soll verbleiben?"),
    html.Label([dcc.Input(id='rest', type='number', min=10, max=1000, step=1, value=50), "mL"]),

    html.H4(id='output-container')
])


@app.callback(
    Output('output-container', 'children'),
    Input('h', 'value'),
    Input('m', 'value'),
    Input('volume', 'value'),
    Input('rest', 'value'),
)
def update_output(h, m, volume, rest):
    #print(h, m, volume, rest)
    flow, difference = timedifference(h, m, volume, rest)
    return (
        "Bei einem Volumen von {} mL, einem gewünschten Restvolumen von {} mL und "
        "einer Ankunft morgen um {}:{} Uhr stelle den Flow auf ".format(volume, rest, h, str(m).zfill(2)), round(flow, 2),
        " ml/min. Bis dahin sind es etwa {}".format(str(round(difference.total_seconds()/3600))), " Stunden.")


def timedifference(h, m, volume, rest):
    now = datetime.today()
    tomorrow = datetime(now.year, now.month, now.day + 1)
    arrival = tomorrow + timedelta(hours=int(h), minutes=int(m))
    difference = (arrival - now)
    voldiff = volume - rest
    flow = voldiff / (difference.total_seconds() // 60)
    return flow, difference


if __name__ == "__main__":
    app.run_server(debug=True)
