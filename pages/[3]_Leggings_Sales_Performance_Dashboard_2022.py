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
        WHERE ii.product_category ILIKE '%legging%'
          AND oi.created_at >= '2022-01-01' AND oi.created_at < '2023-01-01'
        GROUP BY month
        ORDER BY month
    """
    try:
        db_connector = st.session_state['db_connector']
        result = db_connector.execute_query(sql_query)
        df = pd.DataFrame(result, columns=['month', 'leggings_sold'])
        st.subheader('Monthly Leggings Sales Trend')
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['month'], y=df['leggings_sold'], mode='lines+markers', showlegend=False))
        fig.update_layout(
            xaxis=dict(showticklabels=False),
            yaxis_title='Number of Leggings Sold',
            xaxis_title='Month'
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading chart: {e}")


# bar chart

# Which distribution centers sold the most leggings in 2022?

import streamlit as st
import pandas as pd
import plotly.express as px

def top_distribution_centers_leggings_2022():
    sql_query = '''
        SELECT 
            dc.name AS distribution_center_name,
            COUNT(oi.id) AS leggings_sold
        FROM src.order_items oi
        JOIN src.inventory_items ii ON oi.inventory_item_id = ii.id
        JOIN src.products p ON ii.product_id = p.id
        JOIN src.distribution_centres dc ON ii.product_distribution_center_id = dc.id
        WHERE 
            (ii.product_category ILIKE '%legging%' OR ii.product_name ILIKE '%legging%' OR p.category ILIKE '%legging%' OR p.name ILIKE '%legging%')
            AND oi.created_at >= '2022-01-01' AND oi.created_at < '2023-01-01'
        GROUP BY dc.name
        ORDER BY leggings_sold DESC
        LIMIT 10
    '''
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['Distribution Center', 'Leggings Sold'])
        st.subheader('Top Distribution Centers by Leggings Sales')
        fig = px.bar(df, x='Distribution Center', y='Leggings Sold')
        fig.update_layout(showlegend=False, xaxis=dict(showticklabels=False))
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading data: {e}")


# pie chart

# What is the sales breakdown of leggings by brand in 2022?

def leggings_sales_by_brand_2022():
    import streamlit as st
    import pandas as pd
    import plotly.express as px
    sql_query = """
        SELECT p.brand AS brand, SUM(oi.sale_price) AS total_sales
        FROM src.order_items oi
        JOIN src.inventory_items ii ON oi.inventory_item_id = ii.id
        JOIN src.products p ON ii.product_id = p.id
        WHERE p.category ILIKE '%legging%'
          AND oi.created_at >= '2022-01-01' AND oi.created_at < '2023-01-01'
          AND oi.status ILIKE '%delivered%'
        GROUP BY p.brand
        ORDER BY total_sales DESC
    """
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['brand', 'total_sales'])
        st.subheader('Leggings Sales by Brand')
        if not df.empty:
            fig = px.pie(df, names='brand', values='total_sales')
            fig.update_layout(showlegend=False)
            fig.update_xaxes(showticklabels=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write('No data available for 2022.')
    except Exception as e:
        st.error(f"Error loading data: {e}")


# bar chart

# Which states had the highest leggings sales in 2022?

import streamlit as st
import pandas as pd
import plotly.express as px

def leggings_sales_by_state_2022():
    sql_query = '''
        SELECT u.state AS state, COUNT(*) AS leggings_sales
        FROM src.order_items oi
        JOIN src.inventory_items ii ON oi.inventory_item_id = ii.id
        JOIN src.products p ON ii.product_id = p.id
        JOIN src.orders o ON oi.order_id = o.order_id
        JOIN src.users u ON o.user_id = u.id
        WHERE p.category ILIKE '%legging%'
          AND oi.created_at >= '2022-01-01' AND oi.created_at < '2023-01-01'
        GROUP BY u.state
        ORDER BY leggings_sales DESC
        LIMIT 20
    '''
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['state', 'leggings_sales'])
        st.subheader('Leggings Sales by State')
        fig = px.bar(df, x='state', y='leggings_sales')
        fig.update_layout(showlegend=False, xaxis=dict(showticklabels=False))
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading leggings sales by state: {e}")


# bar chart

# What was the return rate for leggings orders in 2022?

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def leggings_return_rate_2022():
    sql_query = '''
        SELECT 
            EXTRACT(MONTH FROM oi.created_at) AS month,
            COUNT(*) FILTER (WHERE oi.returned_at IS NOT NULL) AS returned_count,
            COUNT(*) AS total_count,
            CASE WHEN COUNT(*) = 0 THEN 0 ELSE (COUNT(*) FILTER (WHERE oi.returned_at IS NOT NULL)::float / COUNT(*)::float) END AS return_rate
        FROM src.order_items oi
        JOIN src.products p ON oi.product_id = p.id
        WHERE p.category ILIKE '%legging%'
          AND oi.created_at >= '2022-01-01' AND oi.created_at < '2023-01-01'
        GROUP BY month
        ORDER BY month
    '''
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['month', 'returned_count', 'total_count', 'return_rate'])
        st.subheader('Leggings Return Rate by Month')
        fig = go.Figure()
        fig.add_bar(x=df['month'], y=df['return_rate'], name='Return Rate')
        fig.update_layout(
            showlegend=False,
            xaxis=dict(title='Month', showticklabels=False),
            yaxis=dict(title='Return Rate', tickformat='.0%')
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading data: {e}")


columns = 3
