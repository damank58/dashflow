import streamlit as st


st.title("Sales Performance Across Product Categories")

# bar chart

# What are the total sales by product category?

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def total_sales_by_product_category():
    sql_query = """
        SELECT ii.product_category AS category, SUM(oi.sale_price) AS total_sales
        FROM src.order_items oi
        JOIN src.inventory_items ii ON oi.inventory_item_id = ii.id
        WHERE oi.status ILIKE '%delivered%'
        GROUP BY ii.product_category
        ORDER BY total_sales DESC
    """
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['category', 'total_sales'])
        st.subheader('Total Sales by Category')
        fig = go.Figure(
            data=[go.Bar(x=df['category'], y=df['total_sales'], showlegend=False)]
        )
        fig.update_layout(
            xaxis=dict(showticklabels=False),
            yaxis_title='Total Sales',
            xaxis_title='Product Category',
            margin=dict(l=40, r=40, t=40, b=40)
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading data: {e}")


# line chart

# How have sales trended over time for each product category?

import streamlit as st
import pandas as pd
import plotly.express as px

def sales_trend_by_category_over_time():
    sql_query = '''
        SELECT 
            DATE_TRUNC('month', oi.created_at) AS month,
            ii.product_category,
            SUM(oi.sale_price) AS total_sales
        FROM src.order_items oi
        JOIN src.inventory_items ii ON oi.inventory_item_id = ii.id
        WHERE oi.status ILIKE '%delivered%'
        GROUP BY month, ii.product_category
        ORDER BY month, ii.product_category
        LIMIT 500
    '''
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['month', 'product_category', 'total_sales'])
        if not df.empty:
            fig = px.line(
                df,
                x='month',
                y='total_sales',
                color='product_category',
                labels={'month': 'Month', 'total_sales': 'Total Sales', 'product_category': 'Category'}
            )
            fig.update_layout(
                showlegend=False,
                xaxis=dict(showticklabels=False),
                title=None
            )
            st.subheader('Sales Trend by Category Over Time')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.subheader('Sales Trend by Category Over Time')
            st.write('No data available for the selected query.')
    except Exception as e:
        st.subheader('Sales Trend by Category Over Time')
        st.error(f'Error loading data: {e}')


# bar chart

# Which product categories have the highest number of items sold?

def items_sold_by_category():
    import streamlit as st
    import pandas as pd
    import plotly.graph_objects as go
    sql_query = '''
        SELECT ii.product_category AS category, COUNT(oi.id) AS items_sold
        FROM src.order_items oi
        JOIN src.inventory_items ii ON oi.inventory_item_id = ii.id
        WHERE oi.status ILIKE '%delivered%'
        GROUP BY ii.product_category
        ORDER BY items_sold DESC
        LIMIT 20
    '''
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['category', 'items_sold'])
        st.subheader('Items Sold by Category')
        fig = go.Figure(go.Bar(x=df['category'], y=df['items_sold'], showlegend=False))
        fig.update_layout(xaxis=dict(showticklabels=False), yaxis_title='Items Sold')
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading data: {e}")


# bar chart

# What is the average sale price per product category?

import streamlit as st
import pandas as pd
import plotly.express as px

def average_sale_price_by_category():
    sql_query = """
        SELECT 
            ii.product_category AS category, 
            AVG(oi.sale_price) AS average_sale_price
        FROM src.order_items oi
        JOIN src.inventory_items ii ON oi.inventory_item_id = ii.id
        WHERE oi.sale_price IS NOT NULL AND ii.product_category IS NOT NULL
        GROUP BY ii.product_category
        ORDER BY average_sale_price DESC
    """
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['category', 'average_sale_price'])
        st.subheader('Average Sale Price by Category')
        fig = px.bar(df, x='category', y='average_sale_price')
        fig.update_layout(showlegend=False, xaxis=dict(showticklabels=False))
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading data: {e}")


# heatmap

# How do sales by product category vary across distribution centres?

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def category_sales_by_distribution_centre():
    sql_query = '''
        SELECT 
            dc.name AS distribution_centre,
            ii.product_category AS category,
            COUNT(oi.id) AS sales_count
        FROM src.order_items oi
        JOIN src.inventory_items ii ON oi.inventory_item_id = ii.id
        JOIN src.distribution_centres dc ON ii.product_distribution_center_id = dc.id
        WHERE oi.status ILIKE '%delivered%'
        GROUP BY dc.name, ii.product_category
        ORDER BY dc.name, ii.product_category
    '''
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['distribution_centre', 'category', 'sales_count'])
        if df.empty:
            st.write('No data available to display.')
            return
        pivot_df = df.pivot(index='category', columns='distribution_centre', values='sales_count').fillna(0)
        fig = go.Figure(data=go.Heatmap(
            z=pivot_df.values,
            x=pivot_df.columns,
            y=pivot_df.index,
            colorscale='Viridis',
            showscale=False
        ))
        fig.update_layout(
            xaxis=dict(showticklabels=False),
            yaxis_title='Product Category',
            xaxis_title='Distribution Centre',
            showlegend=False,
            margin=dict(l=40, r=40, t=40, b=40)
        )
        st.subheader('Category Sales by Distribution Centre')
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f'Error loading data: {e}')


# bar chart

# What is the return rate for each product category?

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def return_rate_by_category():
    sql_query = """
        SELECT 
            ii.product_category AS category,
            COUNT(oi.id) AS total_orders,
            COUNT(oi.returned_at) AS total_returns,
            CASE WHEN COUNT(oi.id) = 0 THEN 0 
                 ELSE (COUNT(oi.returned_at)::float / COUNT(oi.id)) END AS return_rate
        FROM src.order_items oi
        JOIN src.inventory_items ii ON oi.inventory_item_id = ii.id
        GROUP BY ii.product_category
        ORDER BY return_rate DESC
    """
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['category', 'total_orders', 'total_returns', 'return_rate'])
        st.subheader('Return Rate by Category')
        fig = go.Figure(
            data=[go.Bar(x=df['category'], y=df['return_rate'])]
        )
        fig.update_layout(
            showlegend=False,
            xaxis=dict(showticklabels=False),
            yaxis_title='Return Rate',
            xaxis_title='Product Category'
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading data: {e}")


# indicator

# What is the total sales revenue?

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def show_total_sales_revenue():
    sql_query = """
        SELECT SUM(sale_price) AS total_revenue
        FROM src.order_items
        WHERE status ILIKE '%sold%'
    """
    try:
        db_connector = st.session_state['db_connector']
        result = db_connector.execute_query(sql_query)
        df = pd.DataFrame(result)
        total_revenue = df['total_revenue'].iloc[0] if not df.empty else 0
        st.subheader('Revenue')
        fig = go.Figure(go.Indicator(
            mode = "number",
            value = total_revenue if total_revenue is not None else 0,
            number = {"prefix": "$"}
        ))
        fig.update_layout(
            showlegend=False,
            xaxis=dict(showticklabels=False),
            height=90,
            margin=dict(l=0, r=0, t=0, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error fetching total sales revenue: {e}")


# indicator

# How many unique product categories had sales?

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def unique_product_categories_indicator():
    sql_query = """
        SELECT COUNT(DISTINCT ii.product_category) AS unique_categories
        FROM src.order_items oi
        JOIN src.inventory_items ii ON oi.inventory_item_id = ii.id
        WHERE oi.status ILIKE '%sale%'
    """
    try:
        db_connector = st.session_state['db_connector']
        result = db_connector.execute_query(sql_query)
        df = pd.DataFrame(result, columns=['unique_categories'])
        value = int(df['unique_categories'].iloc[0]) if not df.empty else 0
        st.subheader('Categories')
        fig = go.Figure(go.Indicator(
            mode = "number",
            value = value,
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


columns = 3
col1, col2,  = st.columns(2)
with col1:
	show_total_sales_revenue()
with col2:
	unique_product_categories_indicator()
col1, col2, col3,  = st.columns(columns)
with col1:
	total_sales_by_product_category()
with col2:
	sales_trend_by_category_over_time()
with col3:
	items_sold_by_category()
col4, col5, col6,  = st.columns(columns)
with col4:
	average_sale_price_by_category()
with col5:
	category_sales_by_distribution_centre()
with col6:
	return_rate_by_category()
