import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, dash_table
import dash_bootstrap_components as dbc
import os

# Load data
airport_summary = pd.read_csv('data/airport_summary.csv')
flights_df = pd.read_csv('data/flight_delays.csv')

# KPIs
total_flights = flights_df.shape[0]
delayed_flights = (flights_df['delay_minutes'] > 0).sum()
avg_delay = flights_df.loc[flights_df['delay_minutes'] > 0, 'delay_minutes'].mean()
delay_pct = delayed_flights / total_flights * 100

# Time series: average delay per day
time_series = airport_summary.groupby('date').agg(
    avg_delay=('avg_delay', 'mean'),
    total_flights=('total_flights', 'sum'),
    delayed_flights=('delayed_flights', 'sum')
).reset_index()

# Bar: Delays by airport
bar_airport = airport_summary.groupby('airport').agg(
    avg_delay=('avg_delay', 'mean'),
    total_flights=('total_flights', 'sum'),
    delayed_flights=('delayed_flights', 'sum')
).reset_index()

# Pie: Delay causes
cause_counts = flights_df[flights_df['delay_minutes'] > 0]['delay_cause'].value_counts().reset_index()
cause_counts.columns = ['delay_cause', 'count']

# App
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'Airline Delay Dashboard'

app.layout = dbc.Container([
    html.H1('Airline Delay Dashboard', style={'fontWeight': 'bold', 'marginTop': 20}),
    dbc.Row([
        dbc.Col(html.Div([
            html.H4('Total Flights', style={'fontWeight': 'bold'}),
            html.H2(f"{total_flights:,}")
        ]), width=3),
        dbc.Col(html.Div([
            html.H4('Delayed Flights', style={'fontWeight': 'bold'}),
            html.H2(f"{delayed_flights:,}")
        ]), width=3),
        dbc.Col(html.Div([
            html.H4('Avg Delay (min)', style={'fontWeight': 'bold'}),
            html.H2(f"{avg_delay:.1f}")
        ]), width=3),
        dbc.Col(html.Div([
            html.H4('% Delayed', style={'fontWeight': 'bold'}),
            html.H2(f"{delay_pct:.1f}%")
        ]), width=3),
    ], style={'marginBottom': 30, 'marginTop': 10}),
    dbc.Row([
        dbc.Col(dcc.Graph(
            figure=px.line(time_series, x='date', y='avg_delay',
                title='<b>Average Delay Over Time</b>',
                labels={'avg_delay': 'Avg Delay (min)', 'date': 'Date'},
                template='plotly_white',
            ).update_layout(title_font=dict(size=20, family='Arial', color='black'),
                            legend_title_text='')
        ), width=8),
        dbc.Col(dcc.Graph(
            figure=px.pie(cause_counts, names='delay_cause', values='count',
                title='<b>Delay Causes</b>',
                color_discrete_sequence=px.colors.qualitative.Safe
            ).update_traces(textinfo='percent+label').update_layout(title_font=dict(size=20, family='Arial', color='black'))
        ), width=4),
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(
            figure=px.bar(bar_airport, x='airport', y='avg_delay',
                title='<b>Average Delay by Airport</b>',
                labels={'avg_delay': 'Avg Delay (min)', 'airport': 'Airport'},
                color='airport',
                color_discrete_sequence=px.colors.qualitative.Pastel,
                template='plotly_white',
            ).update_layout(title_font=dict(size=18, family='Arial', color='black'), legend_title_text='')
        ), width=6),
        dbc.Col(dcc.Graph(
            figure=px.bar(bar_airport, x='airport', y='delayed_flights',
                title='<b>Delayed Flights by Airport</b>',
                labels={'delayed_flights': 'Delayed Flights', 'airport': 'Airport'},
                color='airport',
                color_discrete_sequence=px.colors.qualitative.Set2,
                template='plotly_white',
            ).update_layout(title_font=dict(size=18, family='Arial', color='black'), legend_title_text='')
        ), width=6),
    ]),
    html.Hr(),
    html.H4('Sample Flight Delays Table', style={'fontWeight': 'bold', 'marginTop': 20}),
    dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in flights_df.columns],
        data=flights_df.sample(10).to_dict('records'),
        style_table={'overflowX': 'auto'},
        style_header={'fontWeight': 'bold'},
        style_cell={'textAlign': 'left', 'padding': '5px'},
    ),
    html.Br(),
], fluid=True)

if __name__ == '__main__':
    # Run and export dashboard
    app.run(debug=False, port=8050)
    # To export as HTML, use: app.run_server() and then manually export, or use dash's built-in export if available
    # For this script, we will use the following workaround:
    import dash
    from dash import Dash
    from dash.dash import no_update
    import threading
    import time
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    
    # Start the server in a thread
    def run_dash():
        app.run_server(debug=False, port=8050)
    
    thread = threading.Thread(target=run_dash)
    thread.daemon = True
    thread.start()
    time.sleep(5)  # Wait for server to start
    
    # Use selenium to save the dashboard as HTML
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.get('http://localhost:8050')
    with open('outputs/golden_image.html', 'w', encoding='utf-8') as f:
        f.write(driver.page_source)
    driver.quit()
    print('Dashboard exported to outputs/golden_image.html')