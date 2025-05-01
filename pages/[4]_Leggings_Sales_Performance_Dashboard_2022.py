import streamlit as st


st.title("Leggings Sales Performance Dashboard 2022")

# bar chart

# Which distribution centres had the highest leggings sales in 2022?

def top_distribution_centres_leggings_sales_2022():
    sql_query = '''
        SELECT 
            dc.name AS distribution_centre_name,
            COUNT(oi.id) AS leggings_sales
        FROM src.order_items oi
        JOIN src.inventory_items ii ON oi.inventory_item_id = ii.id
        JOIN src.products p ON ii.product_id = p.id
        JOIN src.distribution_centres dc ON ii.product_distribution_center_id = dc.id
        WHERE 
            (ii.product_name ILIKE '%legging%' OR p.name ILIKE '%legging%' OR ii.product_category ILIKE '%legging%' OR p.category ILIKE '%legging%')
            AND oi.created_at >= '2022-01-01' AND oi.created_at < '2023-01-01'
            AND oi.status ILIKE '%delivered%'
        GROUP BY dc.name
        ORDER BY leggings_sales DESC
        LIMIT 10
    '''
    import streamlit as st
    import pandas as pd
    import plotly.graph_objects as go
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['distribution_centre_name', 'leggings_sales'])
        st.subheader('Top Distribution Centres by Leggings Sales')
        fig = go.Figure(go.Bar(
            x=df['distribution_centre_name'],
            y=df['leggings_sales'],
            marker_color='indigo'
        ))
        fig.update_layout(
            showlegend=False,
            xaxis=dict(showticklabels=False),
            yaxis_title='Leggings Sales',
            xaxis_title='Distribution Centre'
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading chart: {e}")


# line chart

# How did monthly leggings sales trend throughout 2022?

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def monthly_leggings_sales_trend_2022():
    sql_query = '''
        SELECT 
            DATE_TRUNC('month', oi.created_at) AS month,
            SUM(oi.sale_price) AS total_sales
        FROM src.order_items oi
        JOIN src.products p ON oi.product_id = p.id
        WHERE p.category ILIKE '%legging%'
          AND oi.created_at >= '2022-01-01'
          AND oi.created_at < '2023-01-01'
        GROUP BY month
        ORDER BY month
    '''
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['month', 'total_sales'])
        st.subheader('Monthly Leggings Sales Trend (2022)')
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['month'], y=df['total_sales'], mode='lines+markers', showlegend=False))
        fig.update_layout(xaxis=dict(showticklabels=False), yaxis_title='Total Sales ($)')
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading chart: {e}")


# Indicator

# What was the total revenue from leggings sales in 2022?

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def total_revenue_leggings_2022():
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
        st.subheader('Total Revenue')
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
        st.error(f"Error: {e}")


# Indicator

# How many leggings units were sold in 2022?

def leggings_units_sold_2022():
    import streamlit as st
    import pandas as pd
    import plotly.graph_objects as go
    sql_query = """
        SELECT COUNT(*) AS units_sold
        FROM src.order_items oi
        JOIN src.inventory_items ii ON oi.inventory_item_id = ii.id
        JOIN src.products p ON ii.product_id = p.id
        WHERE (p.category ILIKE '%legging%' OR p.name ILIKE '%legging%')
          AND oi.created_at >= '2022-01-01' AND oi.created_at < '2023-01-01'
          AND oi.status ILIKE '%delivered%'
    """
    try:
        db_connector = st.session_state['db_connector']
        result = db_connector.execute_query(sql_query)
        df = pd.DataFrame(result, columns=['units_sold'])
        units_sold = int(df['units_sold'].iloc[0]) if not df.empty else 0
        st.subheader('Units Sold')
        fig = go.Figure(go.Indicator(
            mode = "number",
            value = units_sold,
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
col1, col2,  = st.columns(2)
with col1:
	total_revenue_leggings_2022()
with col2:
	leggings_units_sold_2022()
col1, col2, col3,  = st.columns(columns)
with col1:
	top_distribution_centres_leggings_sales_2022()
with col2:
	monthly_leggings_sales_trend_2022()
