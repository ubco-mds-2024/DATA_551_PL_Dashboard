import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
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
    "Burnley": "#6C1D45",
    "Huddersfield": "#0E63AD",
    "Ipswich": "#3a64a3",
    "Portsmouth": "#001489",
    "Wigan": "#0000ff",
    "Nott'm Forest": "#dd0000",
    "Stoke": "#e03a3e",
    "Liverpool": "#c8102E",
    "Luton": "#F78F1E",
    "Man City": "#6CABDD",
    "Sunderland": "black",
    "Leeds": "#FFCD00",
    "Swansea": "black",
    "Chelsea": "#034694",
    "QPR": "#1D5BA4",
    "Bournemouth": "#B50E12",
    "Watford": "#FBEE23",
    "Derby": "black",
    "Charlton": "black",
    "Bolton": "#263c7e",
    "Reading": "#004494",
    "Brighton": "#0057B8",
    "Newcastle": "black",
    "Fulham": "black",
    "West Brom": "#122F67",
    "Middlesborough": "#004494",
    "Norwich": "#00A650",
    "Birmingham": "#0000FF",
    "Blackburn": "#009EE0",
    "Everton": "#003399",
    "Tottenham": "#132257",
    "Hull": "#F18A01",
    "Cardiff": "#0070B5",
    "Aston Villa": "#670e36",
    "Man United": "#DA291C",
    "Crystal Palace": "#1B458F",
    "Arsenal": "#EF0107",
    "Sheffield United": "#EE2737",
    "Southampton": "#d71920",
    "Wolves": "#FDB913",
    "West Ham": "#7A263A",
    "Leicester": "#003090",
    "Brentford": "#D20000",
    "Blackpool": "#F68712"
}

stats = ["Goals", "Wins"]

# set up app and layout / frontend
# ---------------------------------

app = dash.Dash(external_stylesheets = [dbc.themes.BOOTSTRAP])

colmaxht = "85%"

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
                    # value = sorted(list(set(df["Season"])))
                    value = list(set(df["Season"]))
                )
            ], md = 2, style = {"max-height": colmaxht}),
        dbc.Col([
            dcc.Graph(
                id = "pie1",
                style = {"height": "125%"}
            )
        ], md = 4, style = {"max-height": colmaxht}),
        dbc.Col([
            dcc.Graph(
                id = "pie2",
                style = {"height": "125%"}
            )
        ], md = 4, style = {"max-height": colmaxht})
    ], style = {"height": "45%"}),
    dbc.Row([ 
        dcc.Graph(
            id = "timeline1",
            style = {}
        )
    ], style = {"height": "25%"}),
    dbc.Row([ 
        dcc.Graph(
            id = "timeline2",
            style = {}
        )
    ], style = {"height": "25%"})
], style={"height": "85vh"})


# set up callbacks / backend
# ---------------------------------

@app.callback(
    Output("pie1", "figure"),
    Output("pie2", "figure"),
    Output("timeline1", "figure"),
    Output("timeline2", "figure"),
    Input("teams-list", "value"),
    Input("seasons-list", "value"),
    Input("stat-list", "value")
)
def plot_plotly(teamslist, seasonslist, statlist):
    # Filter data
    filtered_df = df[df["Season"].isin(seasonslist)]
    filtered_df = filtered_df[filtered_df["HomeTeam"].isin(teamslist) | filtered_df["AwayTeam"].isin(teamslist)]

    if statlist == "Goals":
        # Calculate goals per team
        filtered_df = filtered_df.copy()
        filtered_df["Team"] = filtered_df.apply(
            lambda row: row["HomeTeam"] if row["HomeTeam"] in teamslist else row["AwayTeam"], axis=1
        )
        filtered_df["Team_Goals"] = filtered_df.apply(
            lambda row: row["FTHG"] if row["HomeTeam"] in teamslist else row["FTAG"], axis=1
        )

        # Aggregate data for charts
        goals_by_team = filtered_df.groupby("Team")["Team_Goals"].sum().reset_index()
        goals_by_season = filtered_df.groupby(["Season", "Team"])["Team_Goals"].sum().reset_index()
        goals_by_date = filtered_df.groupby(["Date", "Team"])["Team_Goals"].sum().reset_index()

        # Pie Chart 1: Total goals by team
        pie1 = px.pie(
            goals_by_team,
            values="Team_Goals",
            names="Team",
            title="Total Goals by Team",
            color="Team",
            color_discrete_map=team_colours
        )

        # Pie Chart 2: Another view (e.g., average goals per match, placeholder)
        # update this one to be total goals grouped by season (still filtered by teams and seasons)
        goals_by_season = filtered_df.groupby(["Season", "Team"])["Team_Goals"].sum().reset_index()

        pie2 = px.pie(
            goals_by_season,
            values="Team_Goals",
            names="Season",  # Use season labels instead of team names
            title="Total Goals per Season",
            color="Season",
            color_discrete_map=team_colours
        )

        # update the timelines below to have:
        # better x-axis labels
        # fixed scaling per unit time (scrolls left and right)

        # Timeline 1: Line chart of goals per season
        timeline1 = px.line(
            goals_by_season,
            x="Season",
            y="Team_Goals",
            color="Team",
            title="Goals per Season",
            color_discrete_map=team_colours,
            height=300
        )
        timeline1.update_traces(opacity=0.5)

        #Adding scrolling here to line chart
        timeline1.update_layout(
            xaxis=dict(
            rangeslider=dict(visible=True),  
            type="category", 
        )
        )

        # Timeline 2: Scatter chart of goals over time
        timeline2 = px.scatter(
            goals_by_date,
            x="Date",
            y="Team_Goals",
            color="Team",
            title="Goals Over Time",
            color_discrete_map=team_colours,
            height=300
        )
        timeline2.update_traces(opacity=0.5, mode="markers")

    elif statlist == "Wins":
        # Calculate wins per team
        filtered_df = filtered_df.copy()
        filtered_df["Winner"] = filtered_df.apply(
            lambda row: row["HomeTeam"] if row["FTHG"] > row["FTAG"] else 
                       (row["AwayTeam"] if row["FTAG"] > row["FTHG"] else "Draw"), axis=1
        )
        wins_by_team = filtered_df[filtered_df["Winner"].isin(teamslist)].groupby("Winner").size().reset_index(name="Wins")
        wins_by_season = filtered_df[filtered_df["Winner"].isin(teamslist)].groupby(["Season", "Winner"]).size().reset_index(name="Wins")
        wins_by_date = filtered_df[filtered_df["Winner"].isin(teamslist)].groupby(["Date", "Winner"]).size().reset_index(name="Wins")

        # Pie Chart 1: Total wins by team
        pie1 = px.pie(
            wins_by_team,
            values="Wins",
            names="Winner",
            title="Total Wins by Team",
            color="Winner",
            color_discrete_map=team_colours
        )

       
        # Pie Chart 2: Total Wins per Season
        wins_by_season = filtered_df[filtered_df["Winner"].isin(teamslist)].groupby(["Season", "Winner"]).size().reset_index(name="Wins")

        pie2 = px.pie(
            wins_by_season,
            values="Wins",
            names="Season",  
            title="Total Wins per Season",
            color="Season",
            color_discrete_map=team_colours
        )



        # Timeline 1: Line chart of wins per season
        timeline1 = px.line(
            wins_by_season,
            x="Season",
            y="Wins",
            color="Winner",
            title="Wins per Season",
            color_discrete_map=team_colours,
            height=300
        )
        timeline1.update_traces(opacity=0.5)

        timeline1.update_layout(
            xaxis=dict(
            rangeslider=dict(visible=True),  
            type="category", 
        )
        )

        # Timeline 2: Scatter chart of wins over time
        timeline2 = px.scatter(
            wins_by_date,
            x="Date",
            y="Wins",
            color="Winner",
            title="Wins Over Time",
            color_discrete_map=team_colours,
            height=300
        )
        timeline2.update_traces(opacity=0.5, mode="markers")

    return pie1, pie2, timeline1, timeline2

if __name__ == "__main__":
   app.run_server(debug=True)