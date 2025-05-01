import streamlit as st


st.title("Leggings Inventory Analysis Dashboard 2024")

# line chart

# What is the monthly inventory level trend for Leggings in 2024?

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def plot_monthly_inventory_leggings_2024():
    sql_query = """
        SELECT 
            DATE_TRUNC('month', created_at) AS month, 
            COUNT(*) AS inventory_level
        FROM src.inventory_items
        WHERE product_category ILIKE '%Leggings%'
          AND created_at >= '2024-01-01' AND created_at < '2025-01-01'
        GROUP BY month
        ORDER BY month
    """
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['month', 'inventory_level'])
        st.subheader('Monthly Inventory Levels for Leggings')
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['month'], y=df['inventory_level'], mode='lines+markers', showlegend=False))
        fig.update_layout(xaxis=dict(showticklabels=False), yaxis_title='Inventory Level', xaxis_title='Month')
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading chart: {e}")


# bar chart

# How are Leggings inventory levels distributed across distribution centres in 2024?

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def leggings_inventory_by_distribution_centre_2024():
    sql_query = '''
        SELECT 
            dc.name AS distribution_centre,
            COUNT(ii.id) AS leggings_inventory_count
        FROM src.inventory_items ii
        JOIN src.distribution_centres dc
            ON ii.product_distribution_center_id = dc.id
        WHERE 
            ii.product_category ILIKE '%Leggings%'
            AND ii.created_at >= '2024-01-01' AND ii.created_at < '2025-01-01'
            AND ii.sold_at IS NULL
        GROUP BY dc.name
        ORDER BY leggings_inventory_count DESC
    '''
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['Distribution Centre', 'Leggings Inventory Count'])
        st.subheader('Inventory by Distribution Centre')
        fig = go.Figure(data=[
            go.Bar(
                x=df['Distribution Centre'],
                y=df['Leggings Inventory Count'],
                showlegend=False
            )
        ])
        fig.update_layout(
            xaxis=dict(showticklabels=False),
            yaxis_title='Leggings Inventory Count',
            xaxis_title='Distribution Centre'
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading data: {e}")


# line chart

# What is the monthly sales volume of Leggings in 2024?

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def monthly_leggings_sales_volume_2024():
    sql_query = '''
        SELECT 
            DATE_TRUNC('month', oi.created_at) AS month,
            COUNT(*) AS sales_volume
        FROM src.order_items oi
        JOIN src.inventory_items ii ON oi.inventory_item_id = ii.id
        JOIN src.products p ON ii.product_id = p.id
        WHERE 
            oi.created_at >= '2024-01-01' AND oi.created_at < '2025-01-01'
            AND (
                p.name ILIKE '%legging%'
                OR ii.product_name ILIKE '%legging%'
                OR p.category ILIKE '%legging%'
                OR ii.product_category ILIKE '%legging%'
            )
        GROUP BY month
        ORDER BY month
    '''
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['month', 'sales_volume'])
        st.subheader('Monthly Leggings Sales Volume')
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['month'], y=df['sales_volume'], mode='lines+markers', name='Sales Volume'))
        fig.update_layout(
            showlegend=False,
            xaxis=dict(showticklabels=False),
            yaxis_title='Sales Volume',
            xaxis_title='Month'
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading chart: {e}")


# bar chart

# What is the return rate of Leggings by month in 2024?

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def monthly_leggings_return_rate_2024():
    sql_query = '''
        WITH leggings_orders AS (
            SELECT oi.id AS order_item_id,
                   oi.created_at,
                   oi.returned_at
            FROM src.order_items oi
            JOIN src.inventory_items ii ON oi.inventory_item_id = ii.id
            WHERE ii.product_category ILIKE '%Leggings%'
              AND oi.created_at >= '2024-01-01'
              AND oi.created_at < '2025-01-01'
        )
        SELECT 
            DATE_TRUNC('month', created_at) AS month,
            COUNT(order_item_id) AS total_orders,
            COUNT(returned_at) FILTER (WHERE returned_at IS NOT NULL) AS returned_orders,
            CASE WHEN COUNT(order_item_id) = 0 THEN 0
                 ELSE (COUNT(returned_at) FILTER (WHERE returned_at IS NOT NULL)::decimal / COUNT(order_item_id)) END AS return_rate
        FROM leggings_orders
        GROUP BY month
        ORDER BY month
    '''
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['month', 'total_orders', 'returned_orders', 'return_rate'])
        if not df.empty:
            df['month'] = pd.to_datetime(df['month'])
            fig = go.Figure()
            fig.add_bar(x=df['month'], y=df['return_rate'])
            fig.update_layout(
                xaxis=dict(showticklabels=False),
                showlegend=False,
                yaxis_title='Return Rate',
                xaxis_title='Month'
            )
            st.subheader('Monthly Leggings Return Rate')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.subheader('Monthly Leggings Return Rate')
            st.write('No data available for 2024.')
    except Exception as e:
        st.error(f'Error loading data: {e}')


# bar chart

# Which Leggings brands had the highest inventory turnover in 2024?

def leggings_inventory_turnover_2024():
    import streamlit as st
    import pandas as pd
    import plotly.express as px
    sql_query = '''
        WITH leggings_inventory AS (
            SELECT 
                ii.product_brand AS brand,
                COUNT(ii.id) AS total_inventory,
                COUNT(oi.id) FILTER (
                    WHERE oi.created_at >= '2024-01-01' AND oi.created_at < '2025-01-01'
                        AND ii.product_category ILIKE '%leggings%'
                        AND ii.product_brand IS NOT NULL
                ) AS sold_count
            FROM src.inventory_items ii
            LEFT JOIN src.order_items oi ON oi.inventory_item_id = ii.id
            WHERE ii.product_category ILIKE '%leggings%'
                AND ii.product_brand IS NOT NULL
            GROUP BY ii.product_brand
        )
        SELECT 
            brand,
            CASE WHEN total_inventory = 0 THEN 0 ELSE (sold_count::float / total_inventory) END AS inventory_turnover
        FROM leggings_inventory
        WHERE total_inventory > 0
        ORDER BY inventory_turnover DESC
        LIMIT 10;
    '''
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['Brand', 'Inventory Turnover'])
        st.subheader('Inventory Turnover by Brand')
        fig = px.bar(df, x='Brand', y='Inventory Turnover')
        fig.update_layout(showlegend=False, xaxis=dict(showticklabels=False))
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading data: {e}")


columns = 3
