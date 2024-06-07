import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Load the data (replace 'your_data_file.csv' with the actual file path)
df = pd.read_csv('https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv')

# Print the first few rows to verify the data is loaded correctly
print(df.head())

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout of the dashboard
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("CO2 Emissions Dashboard"), className="mb-2", style={'textAlign': 'left'})
    ]),
    dbc.Row([
        dbc.Col(html.H4("-Sowmiyanaarayanan"), className="mb-4", style={'textAlign': 'left'})
    ]),
    dbc.Row([
        dbc.Col(dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': country, 'value': country} for country in df['country'].unique()],
            value=df['country'].unique()[0],  # Default to the first country
            clearable=False
        ), width=4)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='co2-graph'), width=6),
        dbc.Col(dcc.Graph(id='population-graph'), width=6)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='co2-per-capita-bar'), width=6),
        dbc.Col(dcc.Graph(id='co2-source-pie'), width=6)
    ])
])

# Define the callback to update the graphs
@app.callback(
    [Output('co2-graph', 'figure'),
     Output('population-graph', 'figure'),
     Output('co2-per-capita-bar', 'figure'),
     Output('co2-source-pie', 'figure')],
    [Input('country-dropdown', 'value')]
)
def update_graphs(selected_country):
    # Filter data by the selected country
    dff = df[df['country'] == selected_country]
    print(f"Filtered data for country {selected_country}:")
    print(dff.head())
    
    # Line Chart: CO2 emissions over time
    fig1 = px.line(dff, x='year', y='co2', title=f'CO2 Emissions Over Time for {selected_country}',
                   labels={'co2': 'CO2 Emissions'}, template='plotly_dark')

    # Line Chart: Population over time
    fig2 = px.line(dff, x='year', y='population', title=f'Population Over Time for {selected_country}',
                   labels={'population': 'Population'}, template='plotly_dark')

    # Bar Chart: CO2 emissions per capita over time
    fig3 = px.bar(dff, x='year', y='co2_per_capita', title=f'CO2 Emissions Per Capita Over Time for {selected_country}',
                  labels={'co2_per_capita': 'CO2 Emissions Per Capita'}, template='plotly_dark')

    # Pie Chart: Share of different CO2 sources in the most recent year
    latest_year_data = dff[dff['year'] == dff['year'].max()].iloc[0]
    sources = ['coal_co2', 'oil_co2', 'gas_co2', 'cement_co2', 'flaring_co2', 'other_industry_co2']
    source_data = {source: latest_year_data[source] for source in sources}
    source_labels = ['Coal', 'Oil', 'Gas', 'Cement', 'Flaring', 'Other Industry']
    fig4 = px.pie(values=source_data.values(), names=source_labels, 
                  title=f'CO2 Emissions Sources for {selected_country} in {latest_year_data["year"]}',
                  template='plotly_dark')

    return fig1, fig2, fig3, fig4

if __name__ == '__main__':
    app.run_server(debug=True)

