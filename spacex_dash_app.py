# Import required libraries
import pandas as pd
import dash
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

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
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                
                                dcc.Dropdown(
                                    id='site-dropdown', 
                                    options = [{'label':'All Sites', 'value': 'All'}, 
                                               {'label':'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                               {'label':'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                               {'label':'KSC LC-39A', 'value': 'KSC LC-39A'},
                                               {'label':'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}],
                                    value = 'All',
                                    placeholder='Select a launch site',
                                    searchable=True
                                    ),
                                
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(
                                    dcc.Graph(
                                        id='success-pie-chart')),
                                
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0,
                                    max=10000,
                                    step=1000,
                                    marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
                                    value=[0, 10000]),
                                
                                html.Br(),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(
                                    dcc.Graph(
                                        id='success-payload-scatter-chart')),
                                ]
                      )

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    filtered_df = spacex_df
    filtered_df['outcome'] = filtered_df['class'].map({1: 'Success', 0: 'Failure'})
    if entered_site == 'All': 
        fig = px.pie(filtered_df, values='class', 
                        names='Launch Site', 
                        title='Total success launches by site') 
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(data_frame=filtered_df, 
                     names='outcome', 
                     title=f'Total Success vs Failure for site {entered_site}',
                     color='outcome',
                     color_discrete_map={'Success': "#636EFA",
                                         'Failure': "#EF553B"})
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'),
    Input(component_id='payload-slider', component_property='value')
)
def update_scatter_plot(selected_site, payload_range):
    # Unpack the slider range
    low, high = payload_range
    
    # Filter by payload
    filter = (
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)
    )
    filtered_df = spacex_df[filter]
    
    # Further filter by site if not ALL
    if selected_site != 'All':
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
        title = f'Correlation between Payload and Success for site {selected_site}'
    else:
        title = 'Correlation between Payload and Success for all Sites'
    
    # Build the scatter plot
    fig = px.scatter(
        data_frame=filtered_df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title=title
    )
    return fig



# Run the app
if __name__ == '__main__':
    app.run()
