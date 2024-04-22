import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Read the spacex launch data into a pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
min_payload = spacex_df['Payload Mass (kg)'].min()
max_payload = spacex_df['Payload Mass (kg)'].max()

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    dcc.Dropdown(
        id='site-dropdown',
        options=[{'label': 'All Sites', 'value': 'ALL'}] +
                [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(id='payload-slider',
                    min=0,
                    max=10000,
                    step=1000,
                    marks={i: f'{i} Kg' for i in range(0, 10001, 1000)},
                    value=[min_payload, max_payload]),
    html.Br(),
    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def update_pie_chart(entered_site):
    if entered_site == 'ALL':
        filtered_df = spacex_df
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
    
    fig = px.pie(filtered_df, values='class', names='class', 
                 title=f"Total Success Launches for {entered_site}")
    return fig

@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_chart(entered_site, payload_range):
    low, high = payload_range
    if entered_site == 'ALL':
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)]
    else:
        filtered_df = spacex_df[(spacex_df['Launch Site'] == entered_site) & 
                                (spacex_df['Payload Mass (kg)'] >= low) & 
                                (spacex_df['Payload Mass (kg)'] <= high)]
    
    fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', 
                     color='Booster Version Category',
                     title=f"Correlation between Payload and Success for {entered_site}")
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
