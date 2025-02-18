import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import altair as alt
import pandas as pd
import os

# read in, import, combine data
# ---------------------------------

seasons = []
rows_total = 0

for season in os.listdir("../data/raw"):
    # print(season)
    if season[-4:] == ".csv":
        seasons.append(pd.read_csv("../data/raw/" + season, on_bad_lines="warn", encoding='windows-1252'))

for season in seasons:
    rows_total += len(season)
    season["Date"] = pd.to_datetime(season["Date"], format = "mixed", dayfirst = True)

df = pd.concat(seasons, axis = 0, ignore_index = True).dropna(axis = 1, how = "all").dropna(axis = 0, how = "all")

print("%.2f %% of original data imported successfully" % (len(df) / rows_total * 100))
print("%i rows dropped." % (rows_total - len(df)))


# set up app and layout / frontend
# ---------------------------------

app = dash.Dash(external_stylesheets = [dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    html.H1("Premier League Dashboard"),
    dbc.Row([
        html.H2("Filters"),
        dbc.Col([
            html.H2("Checklist of teams here")
        ], md = 2),
                dbc.Col([
            html.H2("Checklist of seasons here")
        ], md = 2),
        dbc.Col([
            html.H2("Per team chart here")
        ], md = 4),
        dbc.Col([
            html.H2("Per season chart here")
        ], md = 4)
    ], className = "h-50"),
    dbc.Row([ 
        html.H2("Season by season timeline here")
    ], className = "h-25"),
    dbc.Row([ 
        html.H2("Match by match timeline here")
    ], className = "h-25")
], style={"height": "90vh"})


# set up callbacks / backend
# ---------------------------------

if __name__ == "__main__":
    app.run_server(debug = True)
    


