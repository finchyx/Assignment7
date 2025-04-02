import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

data = {
    "Year": [1930, 1934, 1938, 1950, 1954, 1958, 1962, 1966, 1970, 1974, 1978, 1982, 1986, 1990, 1994, 1998, 2002, 2006, 2010, 2014, 2018],
    "Winner": ["Uruguay", "Italy", "Italy", "Uruguay", "West Germany", "Brazil", "Brazil", "Brazil", "Brazil", "West Germany", "Argentina", "Italy", "Argentina", "West Germany", "Brazil", "France", "Brazil", "Italy", "Spain", "Germany", "France"],
    "RunnerUp": ["Argentina", "Czechoslovakia", "Hungary", "Brazil", "Hungary", "Sweden", "Czechoslovakia", "England", "Italy", "Netherlands", "Netherlands", "West Germany", "Germany", "Argentina", "Italy", "Italy", "Netherlands", "Germany", "Germany", "Netherlands", "Croatia"]
}

df = pd.DataFrame(data)
app = dash.Dash(__name__)
server=app.server
winner_counts = df["Winner"].value_counts().reset_index()
winner_counts.columns = ['Country', 'Wins']
fig = px.choropleth(winner_counts, locations="Country", locationmode="country names", color="Wins",
                    color_continuous_scale="Viridis", title="FIFA World Cup Winners")
app.layout = html.Div([
    html.H1("FIFA World Cup"),
    dcc.Graph(figure=fig),
    dcc.Dropdown(
        id="country-dropdown",
        options=[{'label': country, 'value': country} for country in winner_counts['Country']],
        value='Argentina',
        multi=False,
        placeholder="Select a country"
    ),
    
    html.Div(id="country-output"),
    dcc.Dropdown(
        id="year-dropdown",
        options=[{'label': year, 'value': year} for year in df['Year'].unique()],
        value=2018,
        multi=False,
        placeholder="Select a year"
    ),
    html.Div(id="year-output")
])

@app.callback(
    dash.dependencies.Output("country-output", "children"),
    [dash.dependencies.Input("country-dropdown", "value")]
)
def update_country_output(country):
    count = winner_counts[winner_counts["Country"] == country]["Wins"].values[0]
    return f"{country} has won the World Cup {count} times."

@app.callback(
    dash.dependencies.Output("year-output", "children"),
    [dash.dependencies.Input("year-dropdown", "value")]
)
def update_year_output(year):
    winner = df[df["Year"] == year]["Winner"].values[0]
    runnerup = df[df["Year"] == year]["RunnerUp"].values[0]
    return f"In {year} the winner was {winner} and the runner up was {runnerup}."

if __name__ == '__main__':
    app.run(debug=True)
