import os
from urllib.parse import quote_plus

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
import dash
from dash import dcc, html
import plotly.express as px


# Load environment variables
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD"))
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

# Connect to MySQL
engine = create_engine(
    f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
)


# Query 1: Average Performance by Brand
df_avg_performance = pd.read_sql("""
    SELECT 
        brand,
        ROUND(AVG(performance), 2) AS avg_performance
    FROM laptops
    GROUP BY brand
    ORDER BY avg_performance DESC
""", engine)


# Query 2: Top 5 Laptops per Brand by Performance
df_top5 = pd.read_sql("""
    SELECT * FROM (
        SELECT 
            laptop,
            brand,
            model,
            performance,
            final_price,
            cpu,
            ram,
            storage,
            ROW_NUMBER() OVER(PARTITION BY brand ORDER BY performance DESC) AS rank_id
        FROM laptops
    ) AS ranked_laptops
    WHERE rank_id <= 5
""", engine)


# Query 3: Average Laptop Price by Brand
df_avg_price = pd.read_sql("""
    SELECT 
        brand,
        ROUND(AVG(final_price), 2) AS avg_price,
        COUNT(*) AS total_laptops
    FROM laptops
    GROUP BY brand
    ORDER BY avg_price DESC
""", engine)


# Query 4: Top 10 best value laptops based on performance per dollar
df_best_value = pd.read_sql("""
    SELECT
        laptop,
        brand,
        model,
        cpu,
        ram,
        storage,
        final_price,
        performance,
        ROUND(performance / final_price, 4) AS value_score
    FROM laptops
    WHERE final_price > 0
    ORDER BY value_score DESC
    LIMIT 10
""", engine)


# Graph 1: Average Performance by Brand
fig_bar = px.bar(
    df_avg_performance,
    x="brand",
    y="avg_performance",
    title="Average Performance per Brand",
    labels={
        "avg_performance": "Avg Performance",
        "brand": "Brand"
    },
    template="plotly_white",
    color="brand",
    color_discrete_sequence=px.colors.qualitative.Safe
)

fig_bar.update_layout(
    xaxis_tickangle=-90,
    showlegend=True
)


# Graph 2: Top 5 Laptops Price vs Performance
fig_scatter = px.scatter(
    df_top5,
    x="performance",
    y="final_price",
    color="brand",
    hover_name="laptop",
    hover_data={
        "final_price": ":$,.2f",
        "cpu": True,
        "ram": True,
        "performance": True
    },
    title="Top 5 Laptops: Price vs. Performance",
    labels={
        "performance": "Performance",
        "final_price": "Price (USD)"
    },
    template="plotly_white"
)

fig_scatter.update_traces(
    marker=dict(
        size=10,
        line=dict(width=1, color="DarkSlateGrey")
    )
)


# Graph 3: Average Laptop Price by Brand
fig_avg_price = px.bar(
    df_avg_price,
    x="brand",
    y="avg_price",
    text="avg_price",
    color="avg_price",
    color_continuous_scale="teal",
    title="Average Laptop Price by Brand",
    labels={
        "brand": "Brand",
        "avg_price": "Average Price",
        "total_laptops": "Total Laptops"
    },
    template="plotly_white"
)

fig_avg_price.update_traces(
    texttemplate="%{text:.2f}",
    textposition="outside"
)

fig_avg_price.update_layout(
    xaxis_tickangle=-45,
    coloraxis_showscale=False
)


# Graph 4: Top 10 Best Value Laptops
fig_best_value = px.bar(
    df_best_value,
    x="value_score",
    y="laptop",
    orientation="h",
    color="brand",
    title="Top 10 Best Value Laptops: Performance per Dollar",
    labels={
        "value_score": "Value Score",
        "laptop": "Laptop"
    },
    hover_data={
        "brand": True,
        "model": True,
        "cpu": True,
        "ram": True,
        "storage": True,
        "final_price": ":$,.2f",
        "performance": True,
        "value_score": True
    },
    template="plotly_white"
)

fig_best_value.update_layout(
    yaxis={"categoryorder": "total ascending"}
)


# Build Dash app
app = dash.Dash(__name__)

app.layout = html.Div(
    style={
        "fontFamily": "Arial, sans-serif",
        "backgroundColor": "#f9f9f9",
        "padding": "20px"
    },
    children=[
        html.Header(
            style={
                "textAlign": "center",
                "marginBottom": "40px"
            },
            children=[
                html.H1(
                    "Laptop Market Intelligence",
                    style={
                        "color": "#2c3e50",
                        "margin": "0"
                    }
                ),
                html.P(
                    "Comparative analysis of performance, pricing, and brand rankings",
                    style={
                        "color": "#7f8c8d"
                    }
                )
            ]
        ),

        # First row: performance and price-performance charts
        html.Div(
            style={
                "display": "flex",
                "flexWrap": "wrap",
                "justifyContent": "center",
                "gap": "20px",
                "marginBottom": "20px"
            },
            children=[
                html.Div(
                    style={
                        "flex": "1",
                        "minWidth": "450px",
                        "backgroundColor": "white",
                        "padding": "15px",
                        "borderRadius": "10px",
                        "boxShadow": "0 4px 6px rgba(0,0,0,0.1)"
                    },
                    children=[
                        dcc.Graph(
                            id="bar-chart",
                            figure=fig_bar
                        )
                    ]
                ),

                html.Div(
                    style={
                        "flex": "1",
                        "minWidth": "450px",
                        "backgroundColor": "white",
                        "padding": "15px",
                        "borderRadius": "10px",
                        "boxShadow": "0 4px 6px rgba(0,0,0,0.1)"
                    },
                    children=[
                        dcc.Graph(
                            id="scatter-plot",
                            figure=fig_scatter
                        )
                    ]
                )
            ]
        ),

        # Second row: average price chart
        html.Div(
            style={
                "backgroundColor": "white",
                "padding": "15px",
                "borderRadius": "10px",
                "boxShadow": "0 4px 6px rgba(0,0,0,0.1)",
                "marginTop": "20px"
            },
            children=[
                dcc.Graph(
                    id="avg-price-chart",
                    figure=fig_avg_price
                )
            ]
        ),

        # Third row: best value chart
        html.Div(
            style={
                "backgroundColor": "white",
                "padding": "15px",
                "borderRadius": "10px",
                "boxShadow": "0 4px 6px rgba(0,0,0,0.1)",
                "marginTop": "20px"
            },
            children=[
                dcc.Graph(
                    id="best-value-chart",
                    figure=fig_best_value
                )
            ]
        )
    ]
)


if __name__ == "__main__":
    app.run(debug=True)