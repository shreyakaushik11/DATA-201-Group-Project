import pandas as pd
from sqlalchemy import create_engine
import dash
from dash import dcc, html
import plotly.express as px

# ── Connect to MySQL ───────────────────────────────────────────────────────────
engine = create_engine("mysql+mysqlconnector://root:tromb0n3@localhost/laptops_db")

# ── Query 1: Average price by brand ───────────────────────────────────────────
query1 = pd.read_sql("""
    SELECT brand, 
           ROUND(AVG(final_price), 2) AS avg_price,
           COUNT(*) AS total_laptops
    FROM laptops
    GROUP BY brand
    ORDER BY avg_price DESC
""", engine)

# ── Build chart ────────────────────────────────────────────────────────────────
fig1 = px.bar(
    query1,
    x="brand",
    y="avg_price",
    text="avg_price",
    color="avg_price",
    color_continuous_scale="teal",
    title="Average Laptop Price by Brand",
    labels={"brand": "Brand", "avg_price": "Average Price (€)"}
)
fig1.update_traces(texttemplate="€%{text:.2f}", textposition="outside")
fig1.update_layout(xaxis_tickangle=-45, coloraxis_showscale=False)

# ── Build app ──────────────────────────────────────────────────────────────────
app = dash.Dash(__name__)

app.layout = html.Div([

    html.H1("💻 Laptop Price Dashboard",
            style={"textAlign": "center", "fontFamily": "Arial", 
                   "color": "#2c3e50", "paddingTop": "20px"}),

    html.P("Interactive analysis of laptop pricing across brands, specs and features.",
           style={"textAlign": "center", "fontFamily": "Arial", "color": "#7f8c8d"}),

    html.Hr(),

    # Query 1
    html.H2("Average Price by Brand",
            style={"fontFamily": "Arial", "paddingLeft": "40px", "color": "#2c3e50"}),
    dcc.Graph(figure=fig1),

])

if __name__ == "__main__":
    app.run(debug=True)

