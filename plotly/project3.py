import pymysql
import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px


def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='password',
        database='database',
        cursorclass=pymysql.cursors.DictCursor
    )

def get_data():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Query 1: Average Performance by Brand
            sql_avg = "SELECT brand, AVG(performance) as avg_performance FROM laptops GROUP BY brand"
            cursor.execute(sql_avg)
            df_avg = pd.DataFrame(cursor.fetchall())

            # Query 2: Top 5 Laptops per Brand by Performance
            sql_top5 = """
            SELECT * FROM (
                SELECT 
                    laptop, brand, model, performance, final_price, cpu, ram, storage,
                    ROW_NUMBER() OVER(PARTITION BY brand ORDER BY performance DESC) as rank_id
                FROM laptops
            ) as ranked_laptops
            WHERE rank_id <= 5
            """
            cursor.execute(sql_top5)
            df_top5 = pd.DataFrame(cursor.fetchall())
            
            return df_avg, df_top5
    finally:
        conn.close()

# Load both dataframes
df_avg, df_top5 = get_data()


# Graph 1: Bar Chart
fig_bar = px.bar(
    df_avg, x='brand', y='avg_performance',
    title='Average Performance per Brand',
    labels={'avg_performance': 'Avg Performance', 'brand': 'Brand'},
    template='plotly_white',
    color='brand',
    color_discrete_sequence=px.colors.qualitative.Safe
)

# Graph 2: Scatter Plot
fig_scatter = px.scatter(
    df_top5, x='performance', y='final_price', color='brand',
    hover_name='laptop',
    hover_data={'final_price': ':$,.2f', 'cpu': True, 'ram': True, 'performance': True},
    title='Top 5 Laptops: Price vs. Performance',
    labels={'performance': 'Performance', 'final_price': 'Price (USD)'},
    template='plotly_white'
)
fig_scatter.update_traces(marker=dict(size=10, line=dict(width=1, color='DarkSlateGrey')))

# Adding graphs to plotly dashboard

app = dash.Dash(__name__)

app.layout = html.Div(style={'fontFamily': 'Arial, sans-serif', 'backgroundColor': '#f9f9f9', 'padding': '20px'}, children=[
    
    html.Header(style={'textAlign': 'center', 'marginBottom': '40px'}, children=[
        html.H1("Laptop Market Intelligence", style={'color': '#2c3e50', 'margin': '0'}),
        html.P("Comparative analysis of performance, pricing, and brand rankings", style={'color': '#7f8c8d'})
    ]),

    # Container for both graphs
    html.Div(style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'center', 'gap': '20px'}, children=[
        
        # Column for Bar Chart
        html.Div(style={'flex': '1', 'minWidth': '450px', 'backgroundColor': 'white', 'padding': '15px', 'borderRadius': '10px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'}, children=[
            dcc.Graph(id='bar-chart', figure=fig_bar)
        ]),

        # Column for Scatter Plot
        html.Div(style={'flex': '1', 'minWidth': '450px', 'backgroundColor': 'white', 'padding': '15px', 'borderRadius': '10px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'}, children=[
            dcc.Graph(id='scatter-plot', figure=fig_scatter)
        ])
    ])
])

if __name__ == '__main__':
    app.run(debug=True)