import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import os
import datetime as dt

# read in, import, combine data
# ---------------------------------
seasons = []
rows_total = 0

for season in os.listdir("../data/raw"):
    if season.endswith(".csv"):
        thisseason = pd.read_csv(
            "../data/raw/" + season, 
            on_bad_lines="warn", 
            encoding='windows-1252'
        )
        thisseason["Season"] = season[0:2] + "/" + season[2:4]
        seasons.append(thisseason)

for season in seasons:
    rows_total += len(season)
    season["Date"] = pd.to_datetime(season["Date"], format="mixed", dayfirst=True)

df = pd.concat(seasons, axis=0, ignore_index=True).dropna(axis=1, how="all").dropna(axis=0, how="all")

print("%.2f %% of original data imported successfully" % (len(df) / rows_total * 100))
print("%i rows dropped." % (rows_total - len(df)))

# team codes and colours
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
    "Everton": "#003399",
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

team_colours = {
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

# club locations for the map
club_locations = [
    {"Club": "Man United", "Lat": 53.4631, "Lon": -2.2913},
    {"Club": "Man City", "Lat": 53.4831, "Lon": -2.2004},
    {"Club": "Liverpool", "Lat": 53.4308, "Lon": -2.9608},
    {"Club": "Everton", "Lat": 53.4388, "Lon": -2.9664},
    {"Club": "Chelsea", "Lat": 51.4817, "Lon": -0.1909},
    {"Club": "Arsenal", "Lat": 51.5549, "Lon": -0.1084},
    {"Club": "Tottenham", "Lat": 51.6043, "Lon": -0.0660},
    {"Club": "West Ham", "Lat": 51.5386, "Lon": 0.0166},
    {"Club": "Crystal Palace", "Lat": 51.3983, "Lon": -0.0856},
    {"Club": "Aston Villa", "Lat": 52.5090, "Lon": -1.8847},
    {"Club": "Wolves", "Lat": 52.5903, "Lon": -2.1300},
    {"Club": "Leicester", "Lat": 52.6204, "Lon": -1.1422},
    {"Club": "Nott'm Forest", "Lat": 52.9399, "Lon": -1.1324},
    {"Club": "Newcastle", "Lat": 54.9756, "Lon": -1.6215},
    {"Club": "Leeds", "Lat": 53.7778, "Lon": -1.5721},
    {"Club": "Sheffield", "Lat": 53.3704, "Lon": -1.4715},
    {"Club": "Brighton", "Lat": 50.8616, "Lon": -0.0830},
    {"Club": "Southampton", "Lat": 50.9058, "Lon": -1.3911},
    {"Club": "Bournemouth", "Lat": 50.7352, "Lon": -1.8382},
    {"Club": "Brentford", "Lat": 51.4882, "Lon": -0.2886},
    {"Club": "Burnley", "Lat": 53.7891, "Lon": -2.2302},
    {"Club": "Fulham", "Lat": 51.4745, "Lon": -0.2216},
    {"Club": "Sunderland", "Lat": 54.9145, "Lon": -1.3883},
    {"Club": "Middlesbrough", "Lat": 54.5780, "Lon": -1.2187},
    {"Club": "Derby", "Lat": 52.9150, "Lon": -1.4478},
]

stats = ["Goals", "Wins"]

# set up app and layout / frontend
# ---------------------------------
app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP, "/assets/pl_style.css"],
    title="Premier League Dashboard"
)

colmaxht = "85%"

info_body = html.Div([
    "The Premier League is the top league for the most popular sport in the world.", html.Br(), html.Br(),
    "It is also the strongest football league as measured by ",
    html.A("Opta Power Ratings", href="https://theanalyst.com/2024/10/strongest-leagues-world-football-opta-power-rankings", target="_blank"), ".", html.Br(), html.Br(),
    "It has existed in its current form since 1992, where it split from the English Football League, the oldest association football league in the world (founded in 1888).", html.Br(), html.Br(),
    "In the ",
    html.A("2022/2023 season ", href="https://en.wikipedia.org/wiki/2022%E2%80%9323_Premier_League", target="_blank"),
    " the PL had over 15 million people in attendance and earned €7.1 billion revenue, with 1084 goals scored across 380 games.",
    html.Br(), html.Br(),
    html.H3("League Format"),
    "There are 20 teams in the Premier League. Each team plays one home game and one away game against each other team (38 total per team).", html.Br(), html.Br(),
    "Teams are awarded three points for a win, or one point each for a draw.", html.Br(), html.Br(),
    "There are no play offs or other tournament format -- the club with the highest number of points at the end of the season wins the league.", html.Br(), html.Br(),
    "In the event of a points tie at the end of the season, goal differential is used to decide the winner.", html.Br(), html.Br(),
    "After each season, the bottom three teams on the table are relegated to the next league down the tier structure, the EFL Championship.", html.Br(), html.Br(),
    "Likewise, the top 3 teams from the EFL Championship join the Premier League for the next season."
])

# Map graph for the clubs
mapgraph = dcc.Graph(
    id="map",
    style={"height": "100%"},
    className="pie-container"
)

app.layout = dbc.Container([
    html.H1("Premier League Dashboard"),
    dbc.Row([
        dcc.Dropdown(
            id="stat-list",
            value="Goals",
            options=[{"label": stat, "value": stat} for stat in stats]
        ),
        dbc.Button("Info", id="open", n_clicks=0),
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Premier League Information")),
            dbc.ModalBody([info_body]),
            dbc.ModalFooter(dbc.Button("Close", id="close", className="ms-auto", n_clicks=0))
        ], id="modal", is_open=False),
        dbc.Button("Map", id="openm", n_clicks=0),
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Premier League Clubs Map")),
            dbc.ModalBody([mapgraph]),
            dbc.ModalFooter(dbc.Button("Close", id="closem", className="ms-auto", n_clicks=0))
        ], id="modalm", is_open=False),
        dbc.Col([
            dcc.Checklist(
                id="teams-list",
                options=[{"label": team, "value": team} for team in sorted(team_codes)],
                value=["Arsenal", "Chelsea", "Liverpool", "Man United", "Tottenham", "Man City"],
                className="list-container"
            )
        ], md=2, style={"max-height": colmaxht}),
        dbc.Col([
            dcc.Checklist(
                id="seasons-list",
                options=[{"label": season, "value": season} for season in sorted(df["Season"].unique())],
                value=list(df["Season"].unique()),
                className="list-container"
            )
        ], md=2, style={"max-height": colmaxht}),
        dbc.Col([
            dcc.Graph(
                id="pie1",
                style={"height": "100%"},
                className="pie-container"
            )
        ], md=4, style={"max-height": colmaxht}),
        dbc.Col([
            dcc.Graph(
                id="pie2",
                style={"height": "105%"},
                className="pie-container"
            )
        ], md=4, style={"max-height": colmaxht})
    ], style={"height": "45%"}),
    dbc.Row([
        dcc.Graph(id="timeline1", style={})
    ], style={"height": "25%"}),
    dbc.Row([
        dcc.Graph(id="timeline2", style={})
    ], style={"height": "28%"})
], style={"height": "85vh"})

# set up callbacks / backend
# ---------------------------------

@app.callback(
    Output("pie1", "figure"),
    Output("pie2", "figure"),
    Output("timeline1", "figure"),
    Output("timeline2", "figure"),
    Output("map", "figure"),
    Input("teams-list", "value"),
    Input("seasons-list", "value"),
    Input("stat-list", "value")
)
def update_figures(teamslist, seasonslist, statlist):
    return plot_plotly(teamslist, seasonslist, statlist)

@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")]
)
def toggle_info_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output("modalm", "is_open"),
    [Input("openm", "n_clicks"), Input("closem", "n_clicks")],
    [State("modalm", "is_open")]
)
def toggle_map_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

def plot_plotly(teamslist, seasonslist, statlist):
    # Filter data
    filtered_df = df[df["Season"].isin(seasonslist)]
    filtered_df = filtered_df[
        filtered_df["HomeTeam"].isin(teamslist) | filtered_df["AwayTeam"].isin(teamslist)
    ]

    if statlist == "Goals":
        # Calculate goals per team
        filtered_df = filtered_df.copy()
        filtered_df["Team"] = filtered_df.apply(
            lambda row: row["HomeTeam"] if row["HomeTeam"] in teamslist else row["AwayTeam"],
            axis=1
        )
        filtered_df["Team_Goals"] = filtered_df.apply(
            lambda row: row["FTHG"] if row["HomeTeam"] in teamslist else row["FTAG"],
            axis=1
        )

        # Aggregate data for charts
        goals_by_team = filtered_df.groupby("Team")["Team_Goals"].sum().reset_index()
        goals_by_season = filtered_df.groupby(["Season", "Team"])["Team_Goals"].sum().reset_index()
        goals_by_date = filtered_df.groupby(["Date", "Team"])["Team_Goals"].sum().reset_index()

        # Pie Chart 1: Total Goals by Team
        pie1 = px.pie(
            goals_by_team,
            values="Team_Goals",
            names="Team",
            title="Total Goals by Team",
            color="Team",
            color_discrete_map=team_colours
        )

        # Pie Chart 2: Total Goals per Season
        pie2 = px.pie(
            goals_by_season,
            values="Team_Goals",
            names="Season",
            title="Total Goals per Season",
            color="Season",
            color_discrete_map=team_colours
        )

        # Timeline1: Goals per Season
        timeline1 = px.line(
            goals_by_season,
            x="Season",
            y="Team_Goals",
            color="Team",
            title="Goals per Season",
            color_discrete_map=team_colours,
            height=300,
            labels={"Team_Goals": "Team Goals"}
        )
        timeline1.update_traces(opacity=0.8)
        timeline1.update_layout(
            xaxis=dict(rangeslider=dict(visible=True), type="category"),
            margin=dict(t=100, b=100, l=100, r=60),  # same left margin for alignment
            title_x=0,
            title_xanchor='left'
        )

        # Timeline2: Cumulative Goals Over Time
        home_goals = filtered_df[filtered_df["HomeTeam"].isin(teamslist)][["Date", "HomeTeam", "FTHG"]].rename(
            columns={"HomeTeam": "Team", "FTHG": "Goals"}
        )
        away_goals = filtered_df[filtered_df["AwayTeam"].isin(teamslist)][["Date", "AwayTeam", "FTAG"]].rename(
            columns={"AwayTeam": "Team", "FTAG": "Goals"}
        )
        combined_goals = pd.concat([home_goals, away_goals])
        combined_goals.sort_values(by=["Team", "Date"], inplace=True)
        combined_goals["Cumulative_Goals"] = combined_goals.groupby("Team")["Goals"].cumsum()

        timeline2 = px.line(
            combined_goals,
            x="Date",
            y="Cumulative_Goals",
            color="Team",
            title="Cumulative Goals Over Time",
            color_discrete_map=team_colours,
            line_shape='linear',
            height=300
        )
        timeline2.update_layout(
            margin=dict(t=100, b=100, l=100, r=60),
            title_x=0,
            title_xanchor='left',
            legend=dict(
                title="Team",
                orientation="v",
                x=1.02,
                xanchor="left",
                y=1
            )
        )

    elif statlist == "Wins":
        # Calculate wins per team
        filtered_df = filtered_df.copy()
        filtered_df["Winner"] = filtered_df.apply(
            lambda row: row["HomeTeam"] if row["FTHG"] > row["FTAG"]
            else (row["AwayTeam"] if row["FTAG"] > row["FTHG"] else "Draw"),
            axis=1
        )
        wins_by_team = filtered_df[filtered_df["Winner"].isin(teamslist)].groupby("Winner").size().reset_index(name="Wins")
        wins_by_season = filtered_df[filtered_df["Winner"].isin(teamslist)].groupby(["Season", "Winner"]).size().reset_index(name="Wins")
        wins_by_date = filtered_df[filtered_df["Winner"].isin(teamslist)].groupby(["Date", "Winner"]).size().reset_index(name="Wins")

        # Pie Chart 1: Total Wins by Team
        pie1 = px.pie(
            wins_by_team,
            values="Wins",
            names="Winner",
            title="Total Wins by Team",
            color="Winner",
            color_discrete_map=team_colours
        )

        # Pie Chart 2: Total Wins per Season
        pie2 = px.pie(
            wins_by_season,
            values="Wins",
            names="Season",
            title="Total Wins per Season",
            color="Season",
            color_discrete_map=team_colours
        )

        # Timeline1: Wins per Season
        timeline1 = px.line(
            wins_by_season,
            x="Season",
            y="Wins",
            color="Winner",
            title="Wins per Season",
            color_discrete_map=team_colours,
            height=300
        )
        timeline1.update_traces(opacity=0.8)
        timeline1.update_layout(
            xaxis=dict(rangeslider=dict(visible=True), type="category"),
            margin=dict(t=100, b=100, l=100, r=60),
            title_x=0,
            title_xanchor='left'
        )

        # Timeline2: Cumulative Wins Over Time
        wins_by_date.sort_values(["Winner", "Date"], inplace=True)
        wins_by_date["Cumulative_Wins"] = wins_by_date.groupby("Winner")["Wins"].cumsum()

        timeline2 = px.line(
            wins_by_date,
            x="Date",
            y="Cumulative_Wins",
            color="Winner",
            title="Cumulative Wins Over Time",
            color_discrete_map=team_colours,
            line_shape='linear',
            height=300
        )
        timeline2.update_layout(
            margin=dict(t=100, b=100, l=100, r=60),
            title_x=0,
            title_xanchor='left',
            legend=dict(
                title="Winner",
                orientation="v",
                x=1.02,
                xanchor="left",
                y=1
            )
        )

    # Minimal styling for all charts (unchanged)
    for chart in [pie1, pie2, timeline1, timeline2]:
        chart.update_layout(
            font_family="RHSIV",
            font_color="#37003c",
            title_font_family="RHSIVBold",
            margin=dict(t=40, b=40, l=0, r=0)
        )

    # Create the map using club_locations
    mapdf = pd.DataFrame(club_locations)
    map_fig = px.scatter_mapbox(
        mapdf,
        lat="Lat",
        lon="Lon",
        text="Club",
        hover_name="Club",
        color="Club",
        color_discrete_map=team_colours,
        zoom=5,
        height=700
    )
    map_fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_center={"lat": 53.0, "lon": -1.5}
    )

    return pie1, pie2, timeline1, timeline2, map_fig

if __name__ == "__main__":
    app.run_server(debug=True)
