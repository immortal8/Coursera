# Import required packages
import pandas as pd
import plotly.express as px
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output


# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()



# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                html.Br(),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                dcc.Dropdown(id='site-dropdown',
                                             options=[
                                                 {'label': 'All Sites', 'value': 'ALL'},
                                                 {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                 {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                 {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                 {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                             ],
                                             value='ALL',
                                             placeholder="Select a Launch",
                                             searchable=True ),
                                html.Br(),
                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                dcc.Graph(id='success-pie-chart'),
                                html.Br(),
                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                       100: '100'},
                                                value=[spacex_df['Payload Mass (kg)'].min(), spacex_df['Payload Mass (kg)'].max()]),
                                html.Br(),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                dcc.Graph(id='success-payload-scatter-chart'),
                                html.Br(),

                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered = spacex_df[['Launch Site', 'class']].groupby('Launch Site').sum()
    filtered.reset_index()
    filtered['pct'] = filtered['class'] / spacex_df['class'].sum() * 100

    if entered_site =='ALL':
        name=['CCAFS LC-40','CCAFS SLC-40','KSC LC-39A','VAFB SLC-4E']
        titl= 'Total success launches by site'

    else:
        filtered_by_site = spacex_df[spacex_df['Launch Site'] == entered_site]
        filtered = filtered_by_site[['Flight Number', 'class']].groupby(
            'class').count()
        filtered.reset_index()
        filtered['pct'] = filtered['Flight Number'] / filtered_by_site[
            'Flight Number'].count() * 100
        name = ['0', '1']
        titl= 'Total success launches for site '+str(entered_site)


    fig = px.pie(filtered, values='pct',names=name,title=titl)
    fig.update_layout(transition_duration=500)


    return fig
    # return the outcomes piechart for a selected site


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'),
    Input(component_id='payload-slider', component_property='value')
)
def get_scatter_chart(entered_site, payload):
    low, high = payload
    filtered = spacex_df[(spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)]
    if entered_site =='ALL':
        titl = 'Correlation between Payload and success for all sites'
        pass
    else:
        filtered = filtered[filtered['Launch Site']==entered_site]
        titl = 'Correlation between Payload and success for site ' + str(
            entered_site)

    fig = px.scatter(filtered, x='Payload Mass (kg)', y='class',
                     color="Booster Version Category", title=titl)
    fig.update_layout(transition_duration=500)

    return fig
    # return the outcomes scatterplot for a selected site and payload range


# Run the application
if __name__ == '__main__':
    app.run_server()
