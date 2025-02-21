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

team_colours = { # finish these!
    "Burnley": "black",
    "Huddersfield": "black",
    "Ipswich": "black",
    "Portsmouth": "black",
    "Wigan": "black",
    "Nott'm Forest": "black",
    "Stoke": "black",
    "Liverpool": "darkred",
    "Luton": "black",
    "Man City": "black",
    "Sunderland": "black",
    "Leeds": "black",
    "Swansea": "black",
    "Chelsea": "black",
    "QPR": "black",
    "Bournemouth": "black",
    "Watford": "black",
    "Derby": "black",
    "Charlton": "black",
    "Bolton": "black",
    "Reading": "black",
    "Brighton": "black",
    "Newcastle": "black",
    "Fulham": "black",
    "West Brom": "black",
    "Middlesborough": "black",
    "Norwich": "black",
    "Birmingham": "black",
    "Blackburn": "black",
    "Everton": "black",
    "Tottenham": "navy",
    "Hull": "black",
    "Cardiff": "black",
    "Aston Villa": "black",
    "Man United": "black",
    "Crystal Palace": "black",
    "Arsenal": "red",
    "Sheffield United": "black",
    "Southampton": "black",
    "Wolves": "black",
    "West Ham": "black",
    "Leicester": "black",
    "Brentford": "black",
    "Blackpool": "black"
}

stats = ["Goals", "Wins"]

# set up app and layout / frontend
# ---------------------------------

app = dash.Dash(external_stylesheets = [dbc.themes.BOOTSTRAP])

colmaxht = "90%"

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
                    options = [{"label": team, "value": team} for team in sorted(team_codes)],
                    style = {"overflowY": "scroll", "max-height": "100%", "max-width": "100%"},
                    value = ["Arsenal", "Chelsea", "Liverpool", "Man United", "Tottenham", "Man City"]
                )
            ], md = 2, style = {"max-height": colmaxht}),
            dbc.Col([
                dcc.Checklist(
                    id = "seasons-list",
                    options = [{"label": season, "value": season} for season in sorted(list(set(df["Season"])))],
                    style = {"overflowY": "scroll", "max-height": "100%", "max-width": "100%"},
                    value = sorted(list(set(df["Season"])))
                )
            ], md = 2, style = {"max-height": colmaxht}),
        dbc.Col([
            html.Iframe(
                id = "pie1",
                style = {}
            )
        ], md = 4, style = {"max-height": colmaxht}),
        dbc.Col([
            html.Iframe(
                id = "pie2",
                style = {}
            )
        ], md = 4, style = {"max-height": colmaxht})
    ], style = {"height": "45%"}),
    dbc.Row([ 
        html.Iframe(
            id = "timeline1",
            style = {}
        )
    ], style = {"height": "25%"}),
    dbc.Row([ 
        html.Iframe(
            id = "timeline2",
            style = {}
        )
    ], style = {"height": "25%"})
], style={"height": "95vh"})


# set up callbacks / backend
# ---------------------------------

@app.callback(
    # Output("pie1", "srcDoc"),
    # Output("pie2", "srcDoc"),
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

        t1s = []
        t2s = []

        for team in teamslist:
            filtered_df = filtered_df.copy()
            filtered_df["Team_Goals"] = filtered_df.apply(
            lambda row: row["FTAG"] if row["AwayTeam"] == team else 
                        (row["FTHG"] if row["HomeTeam"] == team else 0), axis = 1)
        
            pie1 = alt.Chart(filtered_df).mark_arc().encode(
            )

            pie2 = alt.Chart(filtered_df).mark_arc().encode(
            )

            t1 = alt.Chart(filtered_df).mark_line(
                color = team_colours[team], opacity = 0.5).encode(
                x = alt.X("Season"),
                y = alt.Y("sum(Team_Goals):Q", title = "Total")
            ).properties(
                height = 110, width = len(seasonslist) * 120
            )

            t1s.append(t1)

            t2 = alt.Chart(filtered_df).mark_circle(
                color = team_colours[team], opacity = 0.5).encode(
                x = alt.X("Date:T"),
                y = alt.Y("sum(Team_Goals):Q", title = "Goals scored"),
                xOffset = "jitter:Q"
            ).properties(
                height = 110, width = len(seasonslist) * 1000
            )

            t2s.append(t2)

    timeline1 = alt.layer(*t1s)
    timeline2 = alt.layer(*t2s)

    # return pie1.to_html(), pie2.to_html()
    return timeline1.to_html(), timeline2.to_html()

if __name__ == "__main__":
    app.run_server(debug = True)