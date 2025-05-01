import streamlit as st


st.title("Sweater Sales Performance Analysis 2022")

# line chart

# What were the monthly sales trends for sweaters in 2022?

def monthly_sweater_sales_trend_2022():
    import streamlit as st
    import pandas as pd
    import plotly.graph_objects as go
    sql_query = '''
        SELECT 
            DATE_TRUNC('month', oi.created_at) AS month,
            COUNT(oi.id) AS sweater_sales
        FROM src.order_items oi
        JOIN src.products p ON oi.product_id = p.id
        WHERE 
            p.category ILIKE '%sweater%'
            AND oi.created_at >= '2022-01-01' AND oi.created_at < '2023-01-01'
        GROUP BY month
        ORDER BY month
    '''
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['month', 'sweater_sales'])
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['month'], y=df['sweater_sales'], mode='lines+markers', name='Sweater Sales'))
        fig.update_layout(
            title='',
            xaxis_title='',
            yaxis_title='Sweater Sales',
            showlegend=False,
            xaxis=dict(showticklabels=False),
            height=400,
            margin=dict(l=0, r=0, t=0, b=0)
        )
        st.subheader('Monthly Sweater Sales Trend')
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading data: {e}")


# bar chart

# Which distribution centres sold the most sweaters in 2022?

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def sweater_sales_by_distribution_centre():
    sql_query = '''
        SELECT 
            dc.name AS distribution_centre_name,
            COUNT(oi.id) AS sweater_sales
        FROM src.order_items oi
        JOIN src.inventory_items ii ON oi.inventory_item_id = ii.id
        JOIN src.products p ON ii.product_id = p.id
        JOIN src.distribution_centres dc ON p.distribution_center_id = dc.id
        WHERE 
            (p.name ILIKE '%sweater%' OR p.category ILIKE '%sweater%' OR ii.product_name ILIKE '%sweater%' OR ii.product_category ILIKE '%sweater%')
            AND oi.created_at >= '2022-01-01' AND oi.created_at < '2023-01-01'
        GROUP BY dc.name
        ORDER BY sweater_sales DESC
        LIMIT 20
    '''
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['distribution_centre_name', 'sweater_sales'])
        st.subheader('Sweater Sales by Distribution Centre')
        fig = go.Figure(data=[go.Bar(
            x=df['distribution_centre_name'],
            y=df['sweater_sales'],
            marker_color='indigo',
            showlegend=False
        )])
        fig.update_layout(
            xaxis=dict(showticklabels=False),
            yaxis_title='Sweater Sales',
            height=400,
            margin=dict(l=40, r=40, t=40, b=40)
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading data: {e}")


# map

# What was the geographic distribution of sweater sales by city in 2022?

import streamlit as st
import pandas as pd
import plotly.express as px

def sweater_sales_by_city_map():
    sql_query = '''
        SELECT 
            u.city AS city, 
            u.latitude AS latitude, 
            u.longitude AS longitude, 
            COUNT(oi.id) AS sweater_sales
        FROM src.order_items oi
        JOIN src.inventory_items ii ON oi.inventory_item_id = ii.id
        JOIN src.products p ON ii.product_id = p.id
        JOIN src.users u ON oi.user_id = u.id
        WHERE 
            p.category ILIKE '%sweater%'
            AND oi.created_at >= '2022-01-01' AND oi.created_at < '2023-01-01'
        GROUP BY u.city, u.latitude, u.longitude
        HAVING COUNT(oi.id) > 0
        ORDER BY sweater_sales DESC
        LIMIT 100
    '''
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['city', 'latitude', 'longitude', 'sweater_sales'])
        st.subheader('Sweater Sales by City')
        if not df.empty:
            fig = px.scatter_mapbox(
                df,
                lat='latitude',
                lon='longitude',
                size='sweater_sales',
                color='sweater_sales',
                hover_name='city',
                size_max=30,
                zoom=2,
                mapbox_style='carto-positron',
                color_continuous_scale='Blues',
            )
            fig.update_layout(showlegend=False, xaxis=dict(showticklabels=False), yaxis=dict(showticklabels=False))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write('No sweater sales data found for 2022.')
    except Exception as e:
        st.error(f'Error loading data: {e}')


# pie chart

# How did sweater sales vary by customer gender in 2022?

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def sweater_sales_by_gender_2022():
    sql_query = '''
        SELECT o.gender, COUNT(*) AS sweater_sales
        FROM src.order_items oi
        JOIN src.orders o ON oi.order_id = o.order_id
        JOIN src.products p ON oi.product_id = p.id
        WHERE p.category ILIKE '%sweater%'
          AND o.created_at >= '2022-01-01' AND o.created_at < '2023-01-01'
          AND o.gender IS NOT NULL
        GROUP BY o.gender
        ORDER BY sweater_sales DESC
    '''
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['gender', 'sweater_sales'])
        st.subheader('Sweater Sales by Gender')
        fig = go.Figure(data=[go.Pie(labels=df['gender'], values=df['sweater_sales'], showlegend=False)])
        fig.update_layout(
            height=90,
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis=dict(showticklabels=False)
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading data: {e}")


# bar chart

# What was the return rate for sweaters sold in 2022?

def sweater_return_rate_2022():
    import streamlit as st
    import pandas as pd
    import plotly.graph_objects as go
    sql_query = """
        SELECT 
            CASE WHEN COUNT(oi.id) = 0 THEN 0 ELSE 
                (COUNT(oi.returned_at) * 1.0 / COUNT(oi.id)) 
            END AS return_rate
        FROM src.order_items oi
        JOIN src.inventory_items ii ON oi.inventory_item_id = ii.id
        JOIN src.products p ON ii.product_id = p.id
        WHERE 
            p.category ILIKE '%sweater%'
            AND oi.created_at >= '2022-01-01' AND oi.created_at < '2023-01-01'
    """
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['return_rate'])
        st.subheader('Sweater Return Rate')
        fig = go.Figure(go.Bar(
            x=['Sweaters'],
            y=df['return_rate'],
            marker_color=['#636EFA']
        ))
        fig.update_layout(
            showlegend=False,
            xaxis=dict(showticklabels=False),
            yaxis_title='Return Rate',
            height=350,
            margin=dict(l=0, r=0, t=0, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error: {e}")


# bar chart

# Which sweater brands had the highest sales in 2022?

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def top_sweater_brands_sales_2022():
    sql_query = """
        SELECT p.brand AS sweater_brand, SUM(oi.sale_price) AS total_sales
        FROM src.order_items oi
        JOIN src.inventory_items ii ON oi.inventory_item_id = ii.id
        JOIN src.products p ON ii.product_id = p.id
        WHERE ii.product_category ILIKE '%sweater%'
          AND oi.created_at >= '2022-01-01' AND oi.created_at < '2023-01-01'
          AND oi.status ILIKE '%delivered%'
        GROUP BY p.brand
        ORDER BY total_sales DESC
        LIMIT 10
    """
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['sweater_brand', 'total_sales'])
        st.subheader('Top Sweater Brands by Sales')
        fig = go.Figure(go.Bar(
            x=df['sweater_brand'],
            y=df['total_sales'],
            marker_color='indigo',
            showlegend=False
        ))
        fig.update_layout(
            xaxis=dict(showticklabels=False),
            yaxis_title='Total Sales',
            height=400,
            margin=dict(l=40, r=40, t=40, b=40)
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading data: {e}")


# Indicator

# What was the total number of sweaters sold in 2022?

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def total_sweaters_sold_2022():
    sql_query = """
        SELECT COUNT(*) AS total_sold
        FROM src.order_items oi
        JOIN src.inventory_items ii ON oi.inventory_item_id = ii.id
        JOIN src.products p ON ii.product_id = p.id
        WHERE ii.product_category ILIKE '%sweater%'
          AND oi.created_at >= '2022-01-01' AND oi.created_at < '2023-01-01'
          AND oi.status ILIKE '%delivered%'
    """
    try:
        db_connector = st.session_state['db_connector']
        result = db_connector.execute_query(sql_query)
        df = pd.DataFrame(result)
        total_sold = int(df['total_sold'].iloc[0]) if not df.empty else 0
        st.subheader('Total Sold')
        fig = go.Figure(go.Indicator(
            mode = "number",
            value = total_sold,
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


# Indicator

# What was the total revenue from sweater sales in 2022?

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def total_revenue_sweater_sales_2022():
    sql_query = '''
        SELECT COALESCE(SUM(oi.sale_price), 0) AS total_revenue
        FROM src.order_items oi
        JOIN src.inventory_items ii ON oi.inventory_item_id = ii.id
        WHERE ii.product_name ILIKE '%sweater%'
          AND oi.created_at >= '2022-01-01' AND oi.created_at < '2023-01-01'
    '''
    try:
        db_connector = st.session_state['db_connector']
        result = db_connector.execute_query(sql_query)
        df = pd.DataFrame(result)
        total_revenue = df['total_revenue'].iloc[0] if not df.empty else 0
        st.subheader('Total Revenue')
        fig = go.Figure(go.Indicator(
            mode = 'number',
            value = total_revenue,
            number = {'prefix': '$', 'valueformat': ',.2f'}
        ))
        fig.update_layout(
            showlegend=False,
            xaxis=dict(showticklabels=False),
            height=90,
            margin=dict(l=0, r=0, t=0, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error fetching data: {e}")


# Indicator

# What was the average sale price of sweaters in 2022?

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def avg_sale_price_sweaters_2022():
    sql_query = """
        SELECT AVG(oi.sale_price) AS avg_sale_price
        FROM src.order_items oi
        JOIN src.inventory_items ii ON oi.inventory_item_id = ii.id
        WHERE ii.product_category ILIKE '%sweater%'
          AND oi.created_at >= '2022-01-01' AND oi.created_at < '2023-01-01'
          AND oi.sale_price IS NOT NULL
    """
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records)
        avg_price = df['avg_sale_price'].iloc[0] if not df.empty else None
        fig = go.Figure(go.Indicator(
            mode = "number",
            value = avg_price if avg_price is not None else 0,
            number = {"prefix": "$", "valueformat": ".2f"},
            title = {"text": "Avg Sale Price"}
        ))
        fig.update_layout(
            showlegend=False,
            xaxis=dict(showticklabels=False),
            height=90,
            margin=dict(l=0, r=0, t=0, b=0)
        )
        st.subheader("Avg Sale Price")
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error: {e}")


# Indicator

# What was the total number of sweater returns in 2022?

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def total_sweater_returns_2022():
    sql_query = '''
        SELECT COUNT(*) AS total_returns
        FROM src.order_items oi
        JOIN src.products p ON oi.product_id = p.id
        WHERE oi.returned_at >= '2022-01-01' AND oi.returned_at < '2023-01-01'
          AND p.name ILIKE '%sweater%'
    '''
    try:
        db_connector = st.session_state['db_connector']
        result = db_connector.execute_query(sql_query)
        df = pd.DataFrame(result, columns=['total_returns'])
        total_returns = int(df['total_returns'].iloc[0]) if not df.empty else 0
        st.subheader('Total Returns')
        fig = go.Figure(go.Indicator(
            mode = 'number',
            value = total_returns,
            number = {'font': {'size': 48}},
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
        st.error(f"Error fetching data: {e}")


# Indicator

# What was the average time from order to delivery for sweaters in 2022?

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def avg_delivery_time_sweaters_2022():
    sql_query = '''
        SELECT 
            AVG(EXTRACT(EPOCH FROM (oi.delivered_at - oi.created_at))/86400.0) AS avg_delivery_days
        FROM src.order_items oi
        JOIN src.products p ON oi.product_id = p.id
        WHERE p.category ILIKE '%sweater%'
          AND oi.created_at >= '2022-01-01' AND oi.created_at < '2023-01-01'
          AND oi.delivered_at IS NOT NULL
          AND oi.created_at IS NOT NULL
    '''
    try:
        db_connector = st.session_state['db_connector']
        result = db_connector.execute_query(sql_query)
        df = pd.DataFrame(result, columns=['avg_delivery_days'])
        avg_days = df['avg_delivery_days'].iloc[0] if not df.empty else None
        st.subheader('Avg Delivery Time')
        fig = go.Figure(go.Indicator(
            mode = "number",
            value = avg_days if avg_days is not None else 0,
            number = {'suffix': ' days'}
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
col1, col2, col3, col4, col5,  = st.columns(5)
with col1:
	total_sweaters_sold_2022()
with col2:
	total_revenue_sweater_sales_2022()
with col3:
	avg_sale_price_sweaters_2022()
with col4:
	total_sweater_returns_2022()
with col5:
	avg_delivery_time_sweaters_2022()
col1, col2, col3,  = st.columns(columns)
with col1:
	monthly_sweater_sales_trend_2022()
with col2:
	sweater_sales_by_distribution_centre()
with col3:
	sweater_sales_by_city_map()
col4, col5, col6,  = st.columns(columns)
with col4:
	sweater_sales_by_gender_2022()
with col5:
	sweater_return_rate_2022()
with col6:
	top_sweater_brands_sales_2022()
