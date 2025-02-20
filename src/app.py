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
        thisseason = pd.read_csv("../data/raw/" + season, on_bad_lines="warn", encoding='windows-1252')
        thisseason["Season"] = str(season[0:2]) + "/" + str(season[2:4])
        seasons.append(thisseason)

for season in seasons:
    rows_total += len(season)
    season["Date"] = pd.to_datetime(season["Date"], format = "mixed", dayfirst = True)

df = pd.concat(seasons, axis = 0, ignore_index = True).dropna(axis = 1, how = "all").dropna(axis = 0, how = "all")

print("%.2f %% of original data imported successfully" % (len(df) / rows_total * 100))
print("%i rows dropped." % (rows_total - len(df)))

team_codes = {
    "Burnley": "BRN",
    "Huddersfield": "HUD",
    "Ipswich": "IPS",
    "Portsmouth": "POR",
    "Wigan": "WIG",
    "Nott'm Forest": "NFO",
    "Stoke": "STO",
    "Liverpool": "LIV",
    "Luton": "LUT",
    "Man City": "MCI",
    "Sunderland": "SUN",
    "Leeds": "LEE",
    "Swansea": "SWA",
    "Chelsea": "CHE",
    "QPR": "QPR",
    "Bournemouth": "BOU",
    "Watford": "WAT",
    "Derby": "DER",
    "Charlton": "CHA",
    "Bolton": "BOL",
    "Reading": "REA",
    "Brighton": "BHA",
    "Newcastle": "NEW",
    "Fulham": "FUL",
    "West Brom": "WBA",
    "Middlesborough": "MID",
    "Norwich": "NOR",
    "Birmingham": "BIR",
    "Blackburn": "BBR",
    "Everton": "EVE",
    "Tottenham": "TOT",
    "Hull": "HUL",
    "Cardiff": "CAR",
    "Aston Villa": "AVL",
    "Man United": "MUN",
    "Crystal Palace": "CRY",
    "Arsenal": "ARS",
    "Sheffield United": "SHU",
    "Southampton": "SOU",
    "Wolves": "WOL",
    "West Ham": "WHU",
    "Leicester": "LEI",
    "Brentford": "BRE",
    "Blackpool": "BLA"
}

stats = ["Goals", "Wins"]

# set up app and layout / frontend
# ---------------------------------

app = dash.Dash(external_stylesheets = [dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    html.H1("Premier League Dashboard"),
    dbc.Row([
            dcc.Dropdown(
                id = "stat-list",
                value = "Goals",
                options = [{"label": stat, "value": stat} for stat in stats]
            ),
            dbc.Col([
                dcc.Checklist(
                    id = "teams-list",
                    options = [{"label": team, "value": team_codes[team]} for team in sorted(team_codes)],
                    style = {"overflowY": "scroll", "max-height": "30%", "max-width": "100%"}
                )
            ], md = 2),
                    dbc.Col([
                dcc.Checklist(
                    id = "seasons-list",
                    options = [{"label": season, "value": season} for season in sorted(list(set(df["Season"])))],
                    style = {"overflowY": "scroll", "max-height": "30%", "max-width": "100%"}
                )
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

@app.callback(
    Output("pie1", "srcDoc"),
    Output("pie2", "srcDoc"),
    Output("timeline1", "srcDoc"),
    Output("timeline2", "srcDoc"),
    Input("teams-list", "value"),
    Input("seasons-list", "value"),
    Input("stat-list", "value")
)
def plot_altair(teamslist, seasonslist, statlist):

    filtered_df = df[df["Season"].isin(seasonslist)]
    filtered_df = filtered_df[filtered_df["HomeTeam"].isin(teamslist) | filtered_df["AwayTeam"].isin(teamslist)]

    if statlist == "Goals":
        pie1 = alt.Chart(filtered_df).mark_arc().encode(
        )

        pie2 = alt.Chart(filtered_df).mark_arc().encode(
        )

        timeline1 = alt.Chart(filtered_df).mark_line().encode(
        )

        timeline2 = alt.Chart(filtered_df).mark_line().encode(
        )

    return pie1.to_html(), pie2.to_html(), timeline1.to_html(), timeline2.to_html()

if __name__ == "__main__":
    app.run_server(debug = True)