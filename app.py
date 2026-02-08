from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px

# Load and prepare data
df = pd.read_csv('formatted_data.csv')
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(by="date")

app = Dash(__name__)

# Application Layout
app.layout = html.Div(id="container", children=[
    html.H1("Pink Morsel Sales Data", id="header"),
    
    html.Div(id="filter-container", children=[
        html.Label("Filter by Region:", id="filter-label"),
        dcc.RadioItems(
            id='region-filter',
            options=[
                {'label': 'North', 'value': 'north'},
                {'label': 'East', 'value': 'east'},
                {'label': 'South', 'value': 'south'},
                {'label': 'West', 'value': 'west'},
                {'label': 'All', 'value': 'all'}
            ],
            value='all',
            inline=True
        ),
    ]),

    dcc.Graph(id='sales-line-chart'),
])

# Callback for filtering the graph
@app.callback(
    Output('sales-line-chart', 'figure'),
    Input('region-filter', 'value')
)
def update_graph(selected_region):
    if selected_region == 'all':
        filtered_df = df
    else:
        filtered_df = df[df['region'] == selected_region]
    
    fig = px.line(
        filtered_df, 
        x="date", 
        y="sales", 
        title=f"Sales Performance: {selected_region.capitalize()}",
        labels={"sales": "Total Sales ($)", "date": "Date"}
    )
    
    # Reference line for the price increase
    fig.add_vline(x="2021-01-15", line_width=2, line_dash="dash", line_color="#e74c3c", 
                  annotation_text="Price Increase")
    
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font_color='#2c3e50',
        margin=dict(l=40, r=40, t=60, b=40)
    )
    
    return fig

if __name__ == '__main__':
    app.run(debug=True)