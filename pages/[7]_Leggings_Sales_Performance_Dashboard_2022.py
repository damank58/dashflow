import streamlit as st


st.title("Leggings Sales Performance Dashboard 2022")

# line chart

# What were the monthly sales trends for leggings in 2022?

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def monthly_leggings_sales_trend_2022():
    sql_query = '''
        SELECT 
            DATE_TRUNC('month', oi.created_at) AS month,
            COUNT(*) AS leggings_sold
        FROM src.order_items oi
        JOIN src.inventory_items ii ON oi.inventory_item_id = ii.id
        WHERE ii.product_category ILIKE '%legging%'
          AND oi.created_at >= '2022-01-01' AND oi.created_at < '2023-01-01'
        GROUP BY month
        ORDER BY month
    '''
    try:
        db_connector = st.session_state['db_connector']
        result = db_connector.execute_query(sql_query)
        df = pd.DataFrame(result, columns=['month', 'leggings_sold'])
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['month'], y=df['leggings_sold'], mode='lines+markers', showlegend=False))
        fig.update_layout(
            xaxis=dict(showticklabels=False),
            yaxis_title='Leggings Sold',
            xaxis_title='Month',
            title=None
        )
        st.subheader('Monthly Leggings Sales Trend')
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading chart: {e}")


# bar chart

# Which distribution centres sold the most leggings in 2022?

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def leggings_sales_by_distribution_centre():
    sql_query = '''
        SELECT dc.name AS distribution_centre, COUNT(oi.id) AS leggings_sold
        FROM src.order_items oi
        JOIN src.inventory_items ii ON oi.inventory_item_id = ii.id
        JOIN src.products p ON ii.product_id = p.id
        JOIN src.distribution_centres dc ON ii.product_distribution_center_id = dc.id
        WHERE p.category ILIKE '%legging%'
          AND oi.created_at >= '2022-01-01' AND oi.created_at < '2023-01-01'
        GROUP BY dc.name
        ORDER BY leggings_sold DESC
        LIMIT 20
    '''
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['distribution_centre', 'leggings_sold'])
        st.subheader('Leggings Sales by Distribution Centre')
        fig = go.Figure(data=[go.Bar(x=df['distribution_centre'], y=df['leggings_sold'])])
        fig.update_layout(showlegend=False, xaxis=dict(showticklabels=False), yaxis_title='Leggings Sold')
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading data: {e}")


# pie chart

# What is the breakdown of leggings sales by brand in 2022?

import streamlit as st
import pandas as pd
import plotly.express as px

def leggings_sales_by_brand_2022():
    sql_query = '''
        SELECT p.brand AS brand, COUNT(oi.id) AS sales_count
        FROM src.order_items oi
        JOIN src.inventory_items ii ON oi.inventory_item_id = ii.id
        JOIN src.products p ON ii.product_id = p.id
        WHERE p.category ILIKE '%legging%'
          AND oi.created_at >= '2022-01-01' AND oi.created_at < '2023-01-01'
          AND oi.status ILIKE '%delivered%'
        GROUP BY p.brand
        ORDER BY sales_count DESC
    '''
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['brand', 'sales_count'])
        st.subheader('Leggings Sales by Brand')
        if not df.empty:
            fig = px.pie(df, names='brand', values='sales_count')
            fig.update_layout(showlegend=False)
            fig.update_xaxes(showticklabels=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write('No data available for 2022.')
    except Exception as e:
        st.error(f'Error loading data: {e}')


# bar chart

# How do leggings sales vary by customer gender in 2022?

def leggings_sales_by_gender_2022():
    sql_query = '''
        SELECT o.gender, COUNT(oi.id) AS leggings_sales
        FROM src.order_items oi
        JOIN src.orders o ON oi.order_id = o.order_id
        JOIN src.products p ON oi.product_id = p.id
        WHERE p.category ILIKE '%legging%'
          AND o.created_at >= '2022-01-01' AND o.created_at < '2023-01-01'
        GROUP BY o.gender
        ORDER BY leggings_sales DESC
    '''
    import streamlit as st
    import pandas as pd
    import plotly.graph_objects as go
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['gender', 'leggings_sales'])
        st.subheader('Leggings Sales by Customer Gender')
        fig = go.Figure(data=[go.Bar(x=df['gender'], y=df['leggings_sales'], showlegend=False)])
        fig.update_layout(xaxis=dict(showticklabels=False))
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading chart: {e}")


# bar chart

# Which cities had the highest leggings sales in 2022?

import streamlit as st
import pandas as pd
import plotly.express as px

def top_cities_leggings_sales_2022():
    sql_query = '''
        SELECT u.city, COUNT(oi.id) AS leggings_sales
        FROM src.order_items oi
        JOIN src.inventory_items ii ON oi.inventory_item_id = ii.id
        JOIN src.products p ON ii.product_id = p.id
        JOIN src.orders o ON oi.order_id = o.order_id
        JOIN src.users u ON o.user_id = u.id
        WHERE p.category ILIKE '%legging%'
          AND oi.created_at >= '2022-01-01' AND oi.created_at < '2023-01-01'
          AND oi.status ILIKE '%delivered%'
        GROUP BY u.city
        ORDER BY leggings_sales DESC
        LIMIT 10
    '''
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['city', 'leggings_sales'])
        st.subheader('Top Cities for Leggings Sales')
        fig = px.bar(df, x='city', y='leggings_sales')
        fig.update_layout(showlegend=False, xaxis=dict(showticklabels=False))
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading data: {e}")


# pie chart

# What was the return rate for leggings orders in 2022?

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def leggings_return_rate_2022():
    sql_query = '''
        SELECT 
            CASE WHEN oi.returned_at IS NOT NULL THEN 'Returned' ELSE 'Not Returned' END AS return_status,
            COUNT(*) AS count
        FROM src.order_items oi
        JOIN src.inventory_items ii ON oi.inventory_item_id = ii.id
        JOIN src.products p ON oi.product_id = p.id
        WHERE 
            ii.product_category ILIKE '%legging%'
            AND oi.created_at >= '2022-01-01' AND oi.created_at < '2023-01-01'
        GROUP BY return_status
    '''
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['return_status', 'count'])
        st.subheader('Leggings Return Rate')
        fig = go.Figure(data=[go.Pie(
            labels=df['return_status'],
            values=df['count'],
            showlegend=False
        )])
        fig.update_layout(
            xaxis=dict(showticklabels=False),
            yaxis=dict(showticklabels=False)
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error: {e}")


# Indicator

# What was the total revenue from leggings sales in 2022?

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def leggings_revenue_2022():
    sql_query = """
        SELECT COALESCE(SUM(oi.sale_price), 0) AS total_revenue
        FROM src.order_items oi
        JOIN src.inventory_items ii ON oi.inventory_item_id = ii.id
        WHERE ii.product_category ILIKE '%legging%'
          AND oi.created_at >= '2022-01-01' AND oi.created_at < '2023-01-01'
          AND oi.status ILIKE '%delivered%'
    """
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records)
        total_revenue = df['total_revenue'].iloc[0] if not df.empty else 0
        st.subheader('Revenue')
        fig = go.Figure(go.Indicator(
            mode = "number",
            value = total_revenue,
            number = {'prefix': "$", 'valueformat': ',.2f'},
            title = {"text": "Total Leggings Revenue (2022)"}
        ))
        fig.update_layout(
            showlegend=False,
            xaxis=dict(showticklabels=False),
            height=90,
            margin=dict(l=0, r=0, t=0, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading data: {e}")


# Indicator

# How many leggings units were sold in 2022?

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def leggings_units_sold_2022():
    sql_query = '''
        SELECT COUNT(*) AS units_sold
        FROM src.order_items oi
        JOIN src.inventory_items ii ON oi.inventory_item_id = ii.id
        JOIN src.products p ON ii.product_id = p.id
        WHERE (p.category ILIKE '%legging%' OR p.name ILIKE '%legging%')
          AND oi.created_at >= '2022-01-01' AND oi.created_at < '2023-01-01'
          AND oi.status ILIKE '%delivered%'
    '''
    try:
        db_connector = st.session_state['db_connector']
        result = db_connector.execute_query(sql_query)
        df = pd.DataFrame(result, columns=['units_sold'])
        units_sold = int(df['units_sold'].iloc[0]) if not df.empty else 0
        st.subheader('Units Sold')
        fig = go.Figure(go.Indicator(
            mode = 'number',
            value = units_sold,
            number = {'font': {'size': 60}},
            domain = {'x': [0, 1], 'y': [0, 1]}
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

# What was the average sale price of leggings in 2022?

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def avg_sale_price_leggings_2022():
    sql_query = """
        SELECT AVG(oi.sale_price) AS avg_price
        FROM src.order_items oi
        JOIN src.inventory_items ii ON oi.inventory_item_id = ii.id
        WHERE ii.product_category ILIKE '%legging%'
          AND oi.created_at >= '2022-01-01' AND oi.created_at < '2023-01-01'
          AND oi.sale_price IS NOT NULL
    """
    try:
        db_connector = st.session_state['db_connector']
        result = db_connector.execute_query(sql_query)
        df = pd.DataFrame(result, columns=['avg_price'])
        avg_price = df['avg_price'].iloc[0] if not df.empty else None
        st.subheader('Avg Price')
        fig = go.Figure(go.Indicator(
            mode = "number",
            value = avg_price if avg_price is not None else 0,
            number = {'prefix': "$", 'valueformat': ".2f"}
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

# How many unique customers purchased leggings in 2022?

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def unique_customers_leggings_2022():
    sql_query = """
        SELECT COUNT(DISTINCT oi.user_id) AS unique_customers
        FROM src.order_items oi
        JOIN src.products p ON oi.product_id = p.id
        WHERE p.category ILIKE '%legging%'
          AND oi.created_at >= '2022-01-01' AND oi.created_at < '2023-01-01'
    """
    try:
        db_connector = st.session_state['db_connector']
        result = db_connector.execute_query(sql_query)
        df = pd.DataFrame(result, columns=['unique_customers'])
        value = int(df['unique_customers'].iloc[0]) if not df.empty else 0
        st.subheader('Customers')
        fig = go.Figure(go.Indicator(
            mode = "number",
            value = value,
            number = {"font": {"size": 48}}
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
col1, col2, col3, col4,  = st.columns(4)
with col1:
	leggings_revenue_2022()
with col2:
	leggings_units_sold_2022()
with col3:
	avg_sale_price_leggings_2022()
with col4:
	unique_customers_leggings_2022()
col1, col2, col3,  = st.columns(columns)
with col1:
	monthly_leggings_sales_trend_2022()
with col2:
	leggings_sales_by_distribution_centre()
with col3:
	leggings_sales_by_brand_2022()
col4, col5, col6,  = st.columns(columns)
with col4:
	leggings_sales_by_gender_2022()
with col5:
	top_cities_leggings_sales_2022()
with col6:
	leggings_return_rate_2022()
