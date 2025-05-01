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
          AND oi.created_at >= '2022-01-01'
          AND oi.created_at < '2023-01-01'
        GROUP BY month
        ORDER BY month
    '''
    try:
        db_connector = st.session_state['db_connector']
        result = db_connector.execute_query(sql_query)
        df = pd.DataFrame(result, columns=['month', 'leggings_sold'])
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['month'], y=df['leggings_sold'], mode='lines+markers', name=''))
        fig.update_layout(
            title='',
            xaxis_title='',
            yaxis_title='Leggings Sold',
            showlegend=False,
            xaxis=dict(showticklabels=False)
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

def top_distribution_centres_leggings_2022():
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
        LIMIT 10
    '''
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['distribution_centre', 'leggings_sold'])
        st.subheader('Top Distribution Centres by Leggings Sales')
        fig = go.Figure(go.Bar(
            x=df['distribution_centre'],
            y=df['leggings_sold'],
            marker_color='indigo'
        ))
        fig.update_layout(
            showlegend=False,
            xaxis=dict(showticklabels=False),
            yaxis_title='Leggings Sold',
            xaxis_title='Distribution Centre',
            margin=dict(l=40, r=20, t=40, b=40)
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading data: {e}")


# pie chart

# How did leggings sales vary by customer gender in 2022?

def leggings_sales_by_gender_2022():
    import streamlit as st
    import pandas as pd
    import plotly.express as px
    sql_query = """
        SELECT o.gender AS gender, COUNT(oi.id) AS sales_count
        FROM src.order_items oi
        JOIN src.orders o ON oi.order_id = o.order_id
        JOIN src.products p ON oi.product_id = p.id
        WHERE p.category ILIKE '%legging%'
          AND o.created_at >= '2022-01-01' AND o.created_at < '2023-01-01'
          AND o.status ILIKE '%delivered%'
        GROUP BY o.gender
        ORDER BY sales_count DESC
    """
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['gender', 'sales_count'])
        st.subheader('Leggings Sales by Gender')
        fig = px.pie(df, names='gender', values='sales_count')
        fig.update_layout(showlegend=False)
        fig.update_xaxes(showticklabels=False)
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading leggings sales by gender: {e}")


# bar chart

# Which leggings brands had the highest sales in 2022?

import streamlit as st
import pandas as pd
import plotly.express as px

def leggings_brand_sales_2022():
    sql_query = '''
        SELECT 
            ii.product_brand AS brand,
            COUNT(oi.id) AS total_sales
        FROM src.order_items oi
        JOIN src.inventory_items ii ON oi.inventory_item_id = ii.id
        WHERE ii.product_category ILIKE '%legging%'
          AND oi.created_at >= '2022-01-01' AND oi.created_at < '2023-01-01'
          AND oi.status ILIKE '%delivered%'
        GROUP BY ii.product_brand
        ORDER BY total_sales DESC
        LIMIT 10
    '''
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['brand', 'total_sales'])
        st.subheader('Leggings Sales by Brand')
        fig = px.bar(df, x='brand', y='total_sales')
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
        JOIN src.products p ON ii.product_id = p.id
        WHERE p.category ILIKE '%legging%'
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


# indicator

# What was the total revenue from leggings sales in 2022?

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def leggings_revenue_2022_indicator():
    sql_query = """
        SELECT COALESCE(SUM(oi.sale_price), 0) AS total_revenue
        FROM src.order_items oi
        JOIN src.inventory_items ii ON oi.inventory_item_id = ii.id
        JOIN src.products p ON ii.product_id = p.id
        WHERE (ii.product_category ILIKE '%legging%' OR ii.product_name ILIKE '%legging%' OR p.category ILIKE '%legging%' OR p.name ILIKE '%legging%')
          AND oi.created_at >= '2022-01-01' AND oi.created_at < '2023-01-01'
          AND oi.status ILIKE '%delivered%'
    """
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records)
        total_revenue = df['total_revenue'].iloc[0] if not df.empty else 0
        fig = go.Figure(go.Indicator(
            mode = "number",
            value = total_revenue,
            number = {"prefix": "$", "valueformat": ",.2f"}
        ))
        fig.update_layout(
            showlegend=False,
            xaxis=dict(showticklabels=False),
            height=90,
            margin=dict(l=0, r=0, t=0, b=0)
        )
        st.subheader("Revenue")
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error: {e}")


# indicator

# How many leggings units were sold in 2022?

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def leggings_units_sold_2022():
    sql_query = """
        SELECT COUNT(*) AS units_sold
        FROM src.order_items oi
        JOIN src.inventory_items ii ON oi.inventory_item_id = ii.id
        JOIN src.products p ON ii.product_id = p.id
        WHERE p.category ILIKE '%legging%'
          AND oi.created_at >= '2022-01-01' AND oi.created_at < '2023-01-01'
          AND oi.status ILIKE '%delivered%'
    """
    try:
        db_connector = st.session_state['db_connector']
        result = db_connector.execute_query(sql_query)
        df = pd.DataFrame(result)
        units_sold = int(df['units_sold'].iloc[0]) if not df.empty else 0
        fig = go.Figure(go.Indicator(
            mode = "number",
            value = units_sold,
            number = {"font": {"size": 48}}
        ))
        fig.update_layout(
            height=90,
            margin=dict(l=0, r=0, t=0, b=0),
            showlegend=False,
            xaxis=dict(showticklabels=False)
        )
        st.subheader("Units Sold")
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error: {e}")


columns = 3
col1, col2,  = st.columns(2)
with col1:
	leggings_revenue_2022_indicator()
with col2:
	leggings_units_sold_2022()
col1, col2, col3,  = st.columns(columns)
with col1:
	monthly_leggings_sales_trend_2022()
with col2:
	top_distribution_centres_leggings_2022()
with col3:
	leggings_sales_by_gender_2022()
col4, col5, col6,  = st.columns(columns)
with col4:
	leggings_brand_sales_2022()
with col5:
	leggings_return_rate_2022()
