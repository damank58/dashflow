import streamlit as st


st.title("2024 Sweater Inventory Performance Overview")

# line chart

# What is the monthly trend of sweater inventory levels throughout 2024?

def monthly_sweater_inventory_trend_2024():
    import streamlit as st
    import pandas as pd
    import plotly.graph_objects as go
    sql_query = """
        SELECT 
            DATE_TRUNC('month', created_at) AS month,
            COUNT(*) AS inventory_level
        FROM src.inventory_items
        WHERE product_category ILIKE '%sweater%'
          AND created_at >= '2024-01-01' AND created_at < '2025-01-01'
        GROUP BY month
        ORDER BY month
    """
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['month', 'inventory_level'])
        st.subheader('Monthly Sweater Inventory Levels')
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['month'], y=df['inventory_level'], mode='lines+markers', name=''))
        fig.update_layout(
            showlegend=False,
            xaxis=dict(showticklabels=False),
            yaxis_title='Inventory Level',
            xaxis_title='Month'
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading chart: {e}")


# bar chart

# How are sweater stocks distributed across distribution centers in 2024?

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def sweater_stock_by_distribution_center_2024():
    sql_query = '''
        SELECT 
            dc.name AS distribution_center_name,
            COUNT(ii.id) AS sweater_stock
        FROM src.inventory_items ii
        JOIN src.distribution_centres dc
            ON ii.product_distribution_center_id = dc.id
        WHERE 
            ii.product_category ILIKE '%sweater%'
            AND ii.created_at >= '2024-01-01' AND ii.created_at < '2025-01-01'
            AND ii.sold_at IS NULL
        GROUP BY dc.name
        ORDER BY sweater_stock DESC
    '''
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['distribution_center_name', 'sweater_stock'])
        st.subheader('Sweater Stock by Distribution Center')
        fig = go.Figure(
            data=[go.Bar(x=df['distribution_center_name'], y=df['sweater_stock'])]
        )
        fig.update_layout(
            showlegend=False,
            xaxis=dict(showticklabels=False),
            yaxis_title='Sweater Stock',
            xaxis_title='Distribution Center'
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading data: {e}")


# bar chart

# Which sweater brands had the highest and lowest inventory turnover in 2024?

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def inventory_turnover_by_sweater_brand():
    sql_query = '''
        WITH sweater_inventory AS (
            SELECT 
                ii.product_brand AS brand,
                COUNT(*) AS total_inventory,
                COUNT(ii.sold_at) FILTER (WHERE ii.sold_at >= '2024-01-01' AND ii.sold_at < '2025-01-01') AS sold_count
            FROM src.inventory_items ii
            WHERE ii.product_category ILIKE '%sweater%'
                AND ii.created_at < '2025-01-01'
            GROUP BY ii.product_brand
        )
        SELECT 
            brand,
            CASE WHEN total_inventory = 0 THEN 0 ELSE (sold_count::float / total_inventory) END AS inventory_turnover
        FROM sweater_inventory
        WHERE total_inventory > 0
        ORDER BY inventory_turnover DESC
    '''
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['brand', 'inventory_turnover'])
        st.subheader('Inventory Turnover by Sweater Brand')
        fig = go.Figure(data=[go.Bar(x=df['brand'], y=df['inventory_turnover'])])
        fig.update_layout(showlegend=False, xaxis=dict(showticklabels=False), yaxis_title='Inventory Turnover')
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading data: {e}")


# map

# What is the geographic distribution of sweater inventory in 2024?

import streamlit as st
import pandas as pd
import plotly.express as px

def plot_sweater_inventory_geographic_distribution_2024():
    sql_query = '''
        SELECT 
            dc.id AS distribution_center_id,
            dc.name AS distribution_center_name,
            dc.latitude,
            dc.longitude,
            COUNT(ii.id) AS sweater_inventory_count
        FROM src.inventory_items ii
        JOIN src.distribution_centres dc ON ii.product_distribution_center_id = dc.id
        WHERE 
            ii.product_category ILIKE '%sweater%'
            AND ii.created_at >= '2024-01-01' AND ii.created_at < '2025-01-01'
            AND ii.sold_at IS NULL
        GROUP BY dc.id, dc.name, dc.latitude, dc.longitude
        ORDER BY sweater_inventory_count DESC
    '''
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=[
            'distribution_center_id', 'distribution_center_name', 'latitude', 'longitude', 'sweater_inventory_count'
        ])
        st.subheader('Geographic Distribution of Sweater Inventory')
        if not df.empty:
            fig = px.scatter_mapbox(
                df,
                lat='latitude',
                lon='longitude',
                size='sweater_inventory_count',
                hover_name='distribution_center_name',
                hover_data={'latitude': True, 'longitude': True, 'sweater_inventory_count': True},
                color_discrete_sequence=['blue'],
                zoom=2,
                height=500
            )
            fig.update_layout(
                mapbox_style='open-street-map',
                showlegend=False,
                margin=dict(l=0, r=0, t=0, b=0),
                xaxis=dict(showticklabels=False),
                yaxis=dict(showticklabels=False)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write('No sweater inventory data found for 2024.')
    except Exception as e:
        st.error(f'Error loading data: {e}')


# stacked bar chart

# How many sweaters were sold, returned, and remaining in inventory each month in 2024?

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def monthly_sweater_sales_returns_inventory():
    sql_query = '''
    WITH sweater_inventory AS (
        SELECT 
            ii.id AS inventory_item_id,
            ii.product_id,
            ii.product_name,
            ii.product_category,
            ii.sold_at,
            ii.created_at
        FROM src.inventory_items ii
        WHERE ii.product_category ILIKE '%sweater%'
    ),
    sold_per_month AS (
        SELECT 
            DATE_TRUNC('month', si.sold_at) AS month,
            COUNT(*) AS sold
        FROM sweater_inventory si
        WHERE si.sold_at IS NOT NULL
          AND si.sold_at >= '2024-01-01' AND si.sold_at < '2025-01-01'
        GROUP BY 1
    ),
    returned_per_month AS (
        SELECT 
            DATE_TRUNC('month', oi.returned_at) AS month,
            COUNT(*) AS returned
        FROM src.order_items oi
        JOIN sweater_inventory si ON oi.inventory_item_id = si.inventory_item_id
        WHERE oi.returned_at IS NOT NULL
          AND oi.returned_at >= '2024-01-01' AND oi.returned_at < '2025-01-01'
        GROUP BY 1
    ),
    inventory_start AS (
        SELECT 
            DATE_TRUNC('month', gs.month) AS month,
            COUNT(*) AS inventory
        FROM (
            SELECT generate_series('2024-01-01'::date, '2024-12-01'::date, interval '1 month') AS month
        ) gs
        JOIN sweater_inventory si ON si.created_at <= gs.month + interval '1 month' - interval '1 day'
        WHERE (si.sold_at IS NULL OR si.sold_at > gs.month + interval '1 month' - interval '1 day')
        GROUP BY 1
    )
    SELECT 
        to_char(gs.month, 'YYYY-MM') AS month,
        COALESCE(spm.sold, 0) AS sold,
        COALESCE(rpm.returned, 0) AS returned,
        COALESCE(inv.inventory, 0) AS inventory_remaining
    FROM (
        SELECT generate_series('2024-01-01'::date, '2024-12-01'::date, interval '1 month') AS month
    ) gs
    LEFT JOIN sold_per_month spm ON gs.month = spm.month
    LEFT JOIN returned_per_month rpm ON gs.month = rpm.month
    LEFT JOIN inventory_start inv ON gs.month = inv.month
    ORDER BY gs.month
    '''
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['month', 'sold', 'returned', 'inventory_remaining'])
        st.subheader('Monthly Sweater Sales, Returns, and Inventory')
        fig = go.Figure()
        fig.add_bar(x=df['month'], y=df['sold'], name='Sold')
        fig.add_bar(x=df['month'], y=df['returned'], name='Returned')
        fig.add_bar(x=df['month'], y=df['inventory_remaining'], name='Inventory Remaining')
        fig.update_layout(barmode='stack', showlegend=False, xaxis=dict(showticklabels=False))
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f'Error: {e}')


columns = 3
