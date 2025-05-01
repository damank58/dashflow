import streamlit as st


st.title("Leggings Sales Performance Dashboard 2022")

# line chart

# What were the monthly sales trends for leggings in 2022?

def monthly_leggings_sales_trend_2022():
    import streamlit as st
    import pandas as pd
    import plotly.graph_objects as go
    sql_query = """
        SELECT 
            DATE_TRUNC('month', oi.created_at) AS month,
            COUNT(*) AS leggings_sold
        FROM src.order_items oi
        JOIN src.inventory_items ii ON oi.inventory_item_id = ii.id
        JOIN src.products p ON ii.product_id = p.id
        WHERE 
            oi.created_at >= '2022-01-01' AND oi.created_at < '2023-01-01'
            AND (p.category ILIKE '%legging%' OR ii.product_category ILIKE '%legging%' OR p.name ILIKE '%legging%' OR ii.product_name ILIKE '%legging%')
        GROUP BY month
        ORDER BY month
    """
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['month', 'leggings_sold'])
        st.subheader('Monthly Leggings Sales Trend')
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['month'], y=df['leggings_sold'], mode='lines+markers', showlegend=False))
        fig.update_layout(
            xaxis=dict(showticklabels=False),
            yaxis_title='Leggings Sold',
            xaxis_title='Month',
            margin=dict(l=40, r=40, t=40, b=40)
        )
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


# bar chart

# What is the sales breakdown of leggings by brand in 2022?

def leggings_sales_by_brand_2022():
    import streamlit as st
    import pandas as pd
    import plotly.graph_objects as go
    sql_query = """
        SELECT p.brand AS brand, COUNT(oi.id) AS sales_count
        FROM src.order_items oi
        JOIN src.inventory_items ii ON oi.inventory_item_id = ii.id
        JOIN src.products p ON ii.product_id = p.id
        WHERE p.category ILIKE '%legging%'
          AND oi.created_at >= '2022-01-01' AND oi.created_at < '2023-01-01'
        GROUP BY p.brand
        ORDER BY sales_count DESC
    """
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['brand', 'sales_count'])
        st.subheader('Leggings Sales by Brand')
        fig = go.Figure(data=[go.Bar(x=df['brand'], y=df['sales_count'])])
        fig.update_layout(showlegend=False, xaxis=dict(showticklabels=False))
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading chart: {e}")


# pie chart

# How do leggings sales vary by customer gender in 2022?

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def leggings_sales_by_gender_2022():
    sql_query = '''
        SELECT o.gender AS customer_gender, COUNT(oi.id) AS leggings_sales_count
        FROM src.order_items oi
        JOIN src.orders o ON oi.order_id = o.order_id
        JOIN src.products p ON oi.product_id = p.id
        WHERE p.category ILIKE '%legging%'
          AND o.created_at >= '2022-01-01' AND o.created_at < '2023-01-01'
        GROUP BY o.gender
        ORDER BY leggings_sales_count DESC
    '''
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['customer_gender', 'leggings_sales_count'])
        st.subheader('Leggings Sales by Customer Gender')
        fig = go.Figure(data=[go.Pie(labels=df['customer_gender'], values=df['leggings_sales_count'], showlegend=False)])
        fig.update_layout(xaxis=dict(showticklabels=False), yaxis=dict(showticklabels=False))
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading chart: {e}")


# map

# Which states had the highest leggings sales in 2022?

import streamlit as st
import pandas as pd
import plotly.express as px

def leggings_sales_by_state_2022():
    sql_query = '''
        SELECT u.state, COUNT(*) AS leggings_sales_count
        FROM src.order_items oi
        JOIN src.inventory_items ii ON oi.inventory_item_id = ii.id
        JOIN src.products p ON ii.product_id = p.id
        JOIN src.orders o ON oi.order_id = o.order_id
        JOIN src.users u ON o.user_id = u.id
        WHERE p.category ILIKE '%legging%'
          AND oi.created_at >= '2022-01-01' AND oi.created_at < '2023-01-01'
        GROUP BY u.state
        HAVING COUNT(*) > 0
        ORDER BY leggings_sales_count DESC
    '''
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['state', 'leggings_sales_count'])
        st.subheader('Leggings Sales by State')
        if not df.empty:
            fig = px.choropleth(
                df,
                locations='state',
                locationmode='USA-states',
                color='leggings_sales_count',
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
            st.write('No data available for leggings sales in 2022.')
    except Exception as e:
        st.error(f"Error loading data: {e}")


columns = 3
