import streamlit as st


st.title("Leggings Inventory Analysis Dashboard 2022")

# line chart

# What is the monthly trend of leggings sold in 2022?

def monthly_leggings_sold_2022():
    import streamlit as st
    import pandas as pd
    import plotly.graph_objects as go
    sql_query = """
        SELECT 
            DATE_TRUNC('month', oi.created_at) AS month,
            COUNT(*) AS leggings_sold
        FROM src.order_items oi
        JOIN src.products p ON oi.product_id = p.id
        WHERE p.category ILIKE '%legging%'
          AND oi.created_at >= '2022-01-01' AND oi.created_at < '2023-01-01'
        GROUP BY month
        ORDER BY month
    """
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['month', 'leggings_sold'])
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['month'], y=df['leggings_sold'], mode='lines+markers', name=''))
        fig.update_layout(
            showlegend=False,
            xaxis=dict(showticklabels=False),
            yaxis_title='Leggings Sold',
            xaxis_title='Month',
            title=None
        )
        st.subheader('Monthly Leggings Sold in 2022')
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading chart: {e}")


# bar chart

# Which distribution centers had the highest leggings inventory turnover in 2022?

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def inventory_turnover_leggings_2022():
    sql_query = '''
        SELECT 
            dc.name AS distribution_center_name,
            COUNT(ii.id)::float / NULLIF(COUNT(DISTINCT ii.product_id),0) AS inventory_turnover
        FROM src.inventory_items ii
        JOIN src.distribution_centres dc ON ii.product_distribution_center_id = dc.id
        WHERE ii.product_category ILIKE '%legging%'
          AND ii.sold_at >= '2022-01-01' AND ii.sold_at < '2023-01-01'
        GROUP BY dc.name
        ORDER BY inventory_turnover DESC
        LIMIT 10
    '''
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=["Distribution Center", "Inventory Turnover"])
        st.subheader("Inventory Turnover by Distribution Center")
        fig = go.Figure(data=[
            go.Bar(
                x=df["Distribution Center"],
                y=df["Inventory Turnover"],
                showlegend=False
            )
        ])
        fig.update_layout(
            xaxis=dict(showticklabels=False),
            yaxis_title="Inventory Turnover"
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading data: {e}")


# map

# How does leggings inventory vary by state in 2022?

import streamlit as st
import pandas as pd
import plotly.express as px

def leggings_inventory_by_state_2022():
    sql_query = '''
        SELECT u.state, COUNT(ii.id) AS leggings_inventory
        FROM src.inventory_items ii
        JOIN src.users u ON ii.product_distribution_center_id IS NOT NULL
        JOIN src.products p ON ii.product_id = p.id
        WHERE ii.created_at >= '2022-01-01' AND ii.created_at < '2023-01-01'
          AND p.category ILIKE '%legging%'
          AND u.state IS NOT NULL AND u.state != ''
        GROUP BY u.state
        ORDER BY leggings_inventory DESC
    '''
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['state', 'leggings_inventory'])
        st.subheader('Leggings Inventory by State')
        if not df.empty:
            fig = px.choropleth(
                df,
                locations='state',
                locationmode='USA-states',
                color='leggings_inventory',
                scope='usa',
                color_continuous_scale='Blues',
            )
            fig.update_layout(
                showlegend=False,
                xaxis=dict(showticklabels=False),
                yaxis=dict(showticklabels=False),
                margin=dict(l=0, r=0, t=0, b=0)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write('No data available for 2022.')
    except Exception as e:
        st.error(f'Error loading data: {e}')


# line chart

# What is the return rate of leggings by month in 2022?

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def monthly_leggings_return_rate_2022():
    sql_query = '''
        SELECT 
            TO_CHAR(oi.created_at, 'YYYY-MM') AS month,
            COUNT(oi.id) AS total_orders,
            COUNT(oi.returned_at) AS total_returns,
            CASE WHEN COUNT(oi.id) = 0 THEN 0 ELSE (COUNT(oi.returned_at)::float / COUNT(oi.id)) END AS return_rate
        FROM src.order_items oi
        JOIN src.products p ON oi.product_id = p.id
        WHERE p.category ILIKE '%legging%'
          AND oi.created_at >= '2022-01-01' AND oi.created_at < '2023-01-01'
        GROUP BY TO_CHAR(oi.created_at, 'YYYY-MM')
        ORDER BY month
    '''
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['month', 'total_orders', 'total_returns', 'return_rate'])
        st.subheader('Monthly Leggings Return Rate')
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['month'], y=df['return_rate'], mode='lines+markers', name='Return Rate'))
        fig.update_layout(
            showlegend=False,
            xaxis=dict(title='Month', showticklabels=False),
            yaxis=dict(title='Return Rate')
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading chart: {e}")


# pie chart

# What is the distribution of leggings sales by gender in 2022?

def leggings_sales_by_gender_2022():
    import streamlit as st
    import pandas as pd
    import plotly.express as px
    sql_query = """
        SELECT o.gender, COUNT(*) AS sales_count
        FROM src.order_items oi
        JOIN src.orders o ON oi.order_id = o.order_id
        JOIN src.products p ON oi.product_id = p.id
        WHERE p.category ILIKE '%legging%'
          AND oi.created_at >= '2022-01-01' AND oi.created_at < '2023-01-01'
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
        fig.update_traces(textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading chart: {e}")


# Indicator

# What is the total number of leggings sold in 2022?

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def total_leggings_sold_2022():
    sql_query = """
        SELECT COUNT(*) AS total_sold
        FROM src.order_items oi
        JOIN src.inventory_items ii ON oi.inventory_item_id = ii.id
        JOIN src.products p ON ii.product_id = p.id
        WHERE ii.product_category ILIKE '%legging%'
          AND oi.created_at >= '2022-01-01' AND oi.created_at < '2023-01-01'
          AND oi.status ILIKE '%sold%'
    """
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records)
        total_sold = int(df['total_sold'].iloc[0]) if not df.empty else 0
        st.subheader('Total Sold')
        fig = go.Figure(go.Indicator(
            mode = "number",
            value = total_sold,
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


# Indicator

# What is the total leggings inventory at year-end 2022?

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def year_end_2022_leggings_inventory():
    sql_query = """
        SELECT COUNT(*) AS total_leggings_inventory
        FROM src.inventory_items
        WHERE product_category ILIKE '%legging%'
          AND created_at <= '2022-12-31 23:59:59'
          AND (sold_at IS NULL OR sold_at > '2022-12-31 23:59:59')
    """
    try:
        db_connector = st.session_state['db_connector']
        result = db_connector.execute_query(sql_query)
        df = pd.DataFrame(result, columns=['total_leggings_inventory'])
        total_inventory = int(df['total_leggings_inventory'].iloc[0])
        st.subheader('Year-End Inventory')
        fig = go.Figure(go.Indicator(
            mode = "number",
            value = total_inventory,
            number = {"font": {"size": 48}},
            title = {"text": "Leggings"}
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

# What is the total revenue from leggings in 2022?

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def show_leggings_revenue_2022():
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
        df = db_connector.execute_query(sql_query)
        total_revenue = df['total_revenue'].iloc[0] if not df.empty else 0
        st.subheader('Revenue')
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
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading revenue data: {e}")


# Indicator

# What is the leggings return rate in 2022?

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def leggings_return_rate_2022():
    sql_query = """
        SELECT 
            CASE WHEN COUNT(*) = 0 THEN 0 ELSE 
                (SUM(CASE WHEN oi.returned_at IS NOT NULL THEN 1 ELSE 0 END)::float / COUNT(*)) * 100
            END AS return_rate
        FROM src.order_items oi
        JOIN src.inventory_items ii ON oi.inventory_item_id = ii.id
        WHERE ii.product_category ILIKE '%legging%'
          AND oi.created_at >= '2022-01-01' AND oi.created_at < '2023-01-01'
    """
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records)
        return_rate = df['return_rate'].iloc[0] if not df.empty else 0
        fig = go.Figure(go.Indicator(
            mode = "number",
            value = return_rate,
            number = {'suffix': '%', 'font': {'size': 48}},
            title = {'text': "Return Rate"}
        ))
        fig.update_layout(
            showlegend=False,
            xaxis=dict(showticklabels=False),
            height=90,
            margin=dict(l=0, r=0, t=0, b=0)
        )
        st.subheader("Return Rate")
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error: {e}")


columns = 3
col1, col2, col3, col4,  = st.columns(4)
with col1:
	total_leggings_sold_2022()
with col2:
	year_end_2022_leggings_inventory()
with col3:
	show_leggings_revenue_2022()
with col4:
	leggings_return_rate_2022()
col1, col2, col3,  = st.columns(columns)
with col1:
	monthly_leggings_sold_2022()
with col2:
	inventory_turnover_leggings_2022()
with col3:
	leggings_inventory_by_state_2022()
col4, col5, col6,  = st.columns(columns)
with col4:
	monthly_leggings_return_rate_2022()
with col5:
	leggings_sales_by_gender_2022()
