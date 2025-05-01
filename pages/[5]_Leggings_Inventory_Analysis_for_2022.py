import streamlit as st


st.title("Leggings Inventory Analysis for 2022")

# line chart

# What was the monthly inventory level of Leggings throughout 2022?

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def monthly_inventory_level_leggings_2022():
    sql_query = """
        SELECT 
            DATE_TRUNC('month', created_at) AS month,
            COUNT(*) AS inventory_level
        FROM src.inventory_items
        WHERE product_name ILIKE '%Leggings%'
          AND created_at >= '2022-01-01' AND created_at < '2023-01-01'
        GROUP BY month
        ORDER BY month
    """
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['month', 'inventory_level'])
        st.subheader('Monthly Inventory Levels')
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['month'], y=df['inventory_level'], mode='lines+markers', name=''))
        fig.update_layout(showlegend=False, xaxis=dict(showticklabels=False), yaxis_title='Inventory Level', xaxis_title='Month')
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading chart: {e}")


# bar chart

# How many Leggings were sold each month in 2022?

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def monthly_leggings_sold_bar_chart():
    sql_query = '''
        SELECT 
            DATE_TRUNC('month', oi.created_at) AS month,
            COUNT(*) AS leggings_sold
        FROM src.order_items oi
        JOIN src.products p ON oi.product_id = p.id
        WHERE p.name ILIKE '%Legging%'
          AND oi.created_at >= '2022-01-01'
          AND oi.created_at < '2023-01-01'
        GROUP BY month
        ORDER BY month
    '''
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['month', 'leggings_sold'])
        st.subheader('Monthly Leggings Sold')
        fig = go.Figure(data=[
            go.Bar(x=df['month'], y=df['leggings_sold'], showlegend=False)
        ])
        fig.update_layout(
            xaxis=dict(showticklabels=False),
            yaxis_title='Leggings Sold',
            xaxis_title='Month'
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading chart: {e}")


# map

# What is the distribution of Leggings inventory across distribution centres in 2022?

import streamlit as st
import pandas as pd
import plotly.express as px

def inventory_distribution_leggings_2022():
    sql_query = '''
        SELECT 
            dc.id AS distribution_centre_id,
            dc.name AS distribution_centre_name,
            dc.latitude,
            dc.longitude,
            COUNT(ii.id) AS leggings_inventory_count
        FROM src.inventory_items ii
        JOIN src.distribution_centres dc
            ON ii.product_distribution_center_id = dc.id
        WHERE ii.product_category ILIKE '%Leggings%'
          AND ii.created_at >= '2022-01-01' AND ii.created_at < '2023-01-01'
        GROUP BY dc.id, dc.name, dc.latitude, dc.longitude
        ORDER BY leggings_inventory_count DESC
    '''
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=[
            'distribution_centre_id', 'distribution_centre_name', 'latitude', 'longitude', 'leggings_inventory_count'
        ])
        st.subheader('Inventory by Distribution Centre')
        if not df.empty:
            fig = px.scatter_mapbox(
                df,
                lat='latitude',
                lon='longitude',
                size='leggings_inventory_count',
                hover_name='distribution_centre_name',
                hover_data={'leggings_inventory_count': True, 'latitude': False, 'longitude': False},
                color='leggings_inventory_count',
                color_continuous_scale=px.colors.sequential.Blues,
                size_max=30,
                zoom=3,
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
            st.write('No inventory data for Leggings in 2022.')
    except Exception as e:
        st.error(f'Error loading data: {e}')


# line chart

# What was the return rate for Leggings by month in 2022?

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def monthly_return_rate_leggings_2022():
    sql_query = '''
        SELECT 
            DATE_TRUNC('month', oi.created_at) AS month,
            COUNT(CASE WHEN oi.returned_at IS NOT NULL THEN 1 END)::float / NULLIF(COUNT(*),0) AS return_rate
        FROM src.order_items oi
        JOIN src.inventory_items ii ON oi.inventory_item_id = ii.id
        JOIN src.products p ON ii.product_id = p.id
        WHERE p.category ILIKE '%Leggings%'
          AND oi.created_at >= '2022-01-01' AND oi.created_at < '2023-01-01'
        GROUP BY month
        ORDER BY month
    '''
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['month', 'return_rate'])
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['month'], y=df['return_rate'], mode='lines+markers', showlegend=False))
        fig.update_layout(
            xaxis=dict(showticklabels=False),
            yaxis_title='Return Rate',
            xaxis_title='Month',
            title=None
        )
        st.subheader('Monthly Return Rate')
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error: {e}")


# line chart

# How did the average sale price of Leggings change over 2022?

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def average_sale_price_leggings_2022():
    sql_query = """
        SELECT 
            DATE_TRUNC('month', oi.created_at) AS month,
            AVG(oi.sale_price) AS avg_sale_price
        FROM src.order_items oi
        JOIN src.products p ON oi.product_id = p.id
        WHERE p.category ILIKE '%Leggings%'
          AND oi.created_at >= '2022-01-01'
          AND oi.created_at < '2023-01-01'
          AND oi.sale_price IS NOT NULL
        GROUP BY month
        ORDER BY month
    """
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['month', 'avg_sale_price'])
        st.subheader('Average Sale Price Over Time')
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['month'], y=df['avg_sale_price'], mode='lines'))
        fig.update_layout(showlegend=False, xaxis=dict(showticklabels=False), yaxis_title='Average Sale Price', xaxis_title='Month')
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading data: {e}")


# bar chart

# Which distribution centre had the highest Leggings sales in 2022?

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def top_distribution_centres_leggings_sales_2022():
    sql_query = '''
        SELECT 
            dc.name AS distribution_centre_name,
            COUNT(oi.id) AS leggings_sales
        FROM src.order_items oi
        JOIN src.inventory_items ii ON oi.inventory_item_id = ii.id
        JOIN src.distribution_centres dc ON ii.product_distribution_center_id = dc.id
        WHERE ii.product_name ILIKE '%Leggings%'
          AND oi.created_at >= '2022-01-01' AND oi.created_at < '2023-01-01'
        GROUP BY dc.name
        ORDER BY leggings_sales DESC
        LIMIT 10
    '''
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['distribution_centre_name', 'leggings_sales'])
        st.subheader('Top Distribution Centres by Sales')
        fig = go.Figure(data=[
            go.Bar(
                x=df['distribution_centre_name'],
                y=df['leggings_sales'],
                marker_color='indigo'
            )
        ])
        fig.update_layout(
            showlegend=False,
            xaxis=dict(showticklabels=False),
            yaxis_title='Leggings Sales',
            xaxis_title='Distribution Centre'
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading data: {e}")


# Indicator

# What was the total number of Leggings in inventory at the start of 2022?

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def opening_stock_leggings_2022():
    sql_query = """
        SELECT COUNT(*) AS opening_stock
        FROM src.inventory_items
        WHERE product_name ILIKE '%Leggings%'
          AND created_at < '2022-01-01'
          AND (sold_at IS NULL OR sold_at >= '2022-01-01')
    """
    try:
        db_connector = st.session_state['db_connector']
        result = db_connector.execute_query(sql_query)
        df = pd.DataFrame(result)
        opening_stock = int(df['opening_stock'].iloc[0]) if not df.empty else 0
        st.subheader('Opening Stock')
        fig = go.Figure(go.Indicator(
            mode = "number",
            value = opening_stock,
            number = {"font": {"size": 48}},
            domain = {'x': [0, 1], 'y': [0, 1]}
        ))
        fig.update_layout(
            showlegend=False,
            xaxis=dict(showticklabels=False),
            yaxis=dict(showticklabels=False),
            height=90,
            margin=dict(l=0, r=0, t=0, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error: {e}")


# Indicator

# What was the total number of Leggings sold in 2022?

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def total_leggings_sold_2022():
    sql_query = """
        SELECT COUNT(*) AS total_sold
        FROM src.inventory_items
        WHERE product_name ILIKE '%Leggings%'
          AND sold_at >= '2022-01-01' AND sold_at < '2023-01-01'
    """
    try:
        db_connector = st.session_state['db_connector']
        result = db_connector.execute_query(sql_query)
        df = pd.DataFrame(result, columns=['total_sold'])
        total_sold = int(df['total_sold'].iloc[0]) if not df.empty else 0
        st.subheader('Total Sold')
        fig = go.Figure(go.Indicator(
            mode = "number",
            value = total_sold,
            number = {"font": {"size": 60}}
        ))
        fig.update_layout(
            showlegend=False,
            xaxis=dict(showticklabels=False),
            height=90,
            margin=dict(l=0, r=0, t=0, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error: {e}")


# Indicator

# What was the total number of Leggings returned in 2022?

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def leggings_returned_2022_indicator():
    sql_query = '''
        SELECT COUNT(*) AS total_returned
        FROM src.order_items oi
        JOIN src.inventory_items ii ON oi.inventory_item_id = ii.id
        WHERE ii.product_name ILIKE '%Leggings%'
          AND oi.returned_at >= '2022-01-01' AND oi.returned_at < '2023-01-01'
    '''
    try:
        db_connector = st.session_state['db_connector']
        result = db_connector.execute_query(sql_query)
        df = pd.DataFrame(result, columns=['total_returned'])
        total_returned = int(df['total_returned'].iloc[0]) if not df.empty else 0
        st.subheader('Total Returned')
        fig = go.Figure(go.Indicator(
            mode = 'number',
            value = total_returned,
            number = {'font': {'size': 60}}
        ))
        fig.update_layout(
            showlegend=False,
            xaxis=dict(showticklabels=False),
            height=90,
            margin=dict(l=0, r=0, t=0, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error: {e}")


columns = 3
col1, col2, col3,  = st.columns(3)
with col1:
	opening_stock_leggings_2022()
with col2:
	total_leggings_sold_2022()
with col3:
	leggings_returned_2022_indicator()
col1, col2, col3,  = st.columns(columns)
with col1:
	monthly_inventory_level_leggings_2022()
with col2:
	monthly_leggings_sold_bar_chart()
with col3:
	inventory_distribution_leggings_2022()
col4, col5, col6,  = st.columns(columns)
with col4:
	monthly_return_rate_leggings_2022()
with col5:
	average_sale_price_leggings_2022()
with col6:
	top_distribution_centres_leggings_sales_2022()
