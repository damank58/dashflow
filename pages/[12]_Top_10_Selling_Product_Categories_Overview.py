import streamlit as st


st.title("Top 10 Selling Product Categories Overview")

# bar chart

# Which are the top 10 product categories by total units sold?

import streamlit as st
import pandas as pd
import plotly.express as px

def top_10_categories_by_units_sold():
    sql_query = """
        SELECT 
            p.category AS product_category, 
            COUNT(oi.id) AS total_units_sold
        FROM src.order_items oi
        JOIN src.products p ON oi.product_id = p.id
        WHERE oi.status ILIKE '%delivered%'
        GROUP BY p.category
        ORDER BY total_units_sold DESC
        LIMIT 10
    """
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=["product_category", "total_units_sold"])
        st.subheader("Top 10 Categories by Units Sold")
        fig = px.bar(df, x="product_category", y="total_units_sold")
        fig.update_layout(showlegend=False, xaxis=dict(showticklabels=False))
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading data: {e}")


# bar chart

# What is the total sales revenue for each of the top 10 product categories?

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def sales_revenue_by_top_10_categories():
    sql_query = """
        SELECT 
            ii.product_category AS category, 
            SUM(oi.sale_price) AS total_sales_revenue
        FROM src.order_items oi
        JOIN src.inventory_items ii ON oi.inventory_item_id = ii.id
        WHERE oi.sale_price IS NOT NULL
        GROUP BY ii.product_category
        ORDER BY total_sales_revenue DESC
        LIMIT 10
    """
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['category', 'total_sales_revenue'])
        st.subheader('Sales Revenue by Category')
        fig = go.Figure(
            data=[go.Bar(x=df['category'], y=df['total_sales_revenue'])]
        )
        fig.update_layout(
            showlegend=False,
            xaxis=dict(showticklabels=False),
            yaxis_title='Total Sales Revenue',
            xaxis_title='Product Category'
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading data: {e}")


# bar chart

# What is the average sale price per item in each of the top 10 categories?

import streamlit as st
import pandas as pd
import plotly.express as px

def average_sale_price_by_category():
    sql_query = """
        SELECT 
            ii.product_category AS category, 
            AVG(oi.sale_price) AS avg_sale_price
        FROM src.order_items oi
        JOIN src.inventory_items ii ON oi.inventory_item_id = ii.id
        WHERE oi.sale_price IS NOT NULL AND ii.product_category IS NOT NULL
        GROUP BY ii.product_category
        ORDER BY avg_sale_price DESC
        LIMIT 10
    """
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['category', 'avg_sale_price'])
        st.subheader('Average Sale Price by Category')
        fig = px.bar(df, x='category', y='avg_sale_price')
        fig.update_layout(showlegend=False, xaxis=dict(showticklabels=False))
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error: {e}")


# stacked bar chart

# Which brands are most popular within the top 10 selling categories?

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def top_brands_in_leading_categories():
    sql_query = '''
        WITH top_categories AS (
            SELECT 
                ii.product_category,
                COUNT(oi.id) AS total_sales
            FROM src.order_items oi
            JOIN src.inventory_items ii ON oi.inventory_item_id = ii.id
            GROUP BY ii.product_category
            ORDER BY total_sales DESC
            LIMIT 10
        )
        SELECT 
            ii.product_category AS category,
            ii.product_brand AS brand,
            COUNT(oi.id) AS sales_count
        FROM src.order_items oi
        JOIN src.inventory_items ii ON oi.inventory_item_id = ii.id
        WHERE ii.product_category IN (SELECT product_category FROM top_categories)
        GROUP BY ii.product_category, ii.product_brand
        ORDER BY ii.product_category, sales_count DESC
    '''
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['category', 'brand', 'sales_count'])
        if df.empty:
            st.write('No data available.')
            return
        pivot_df = df.pivot(index='category', columns='brand', values='sales_count').fillna(0)
        st.subheader('Top Brands in Leading Categories')
        fig = go.Figure()
        for brand in pivot_df.columns:
            fig.add_bar(
                x=pivot_df.index,
                y=pivot_df[brand],
                name=brand
            )
        fig.update_layout(
            barmode='stack',
            showlegend=False,
            xaxis=dict(showticklabels=False),
            yaxis_title='Sales Count',
            xaxis_title='Category'
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f'Error: {e}')


# heatmap

# From which distribution centers are the top 10 categories most frequently shipped?

import streamlit as st
import pandas as pd
import plotly.express as px

def distribution_centers_top_categories_heatmap():
    sql_query = '''
        WITH top_categories AS (
            SELECT ii.product_category
            FROM src.order_items oi
            JOIN src.inventory_items ii ON oi.inventory_item_id = ii.id
            WHERE oi.shipped_at IS NOT NULL
            GROUP BY ii.product_category
            ORDER BY COUNT(*) DESC
            LIMIT 10
        )
        SELECT 
            dc.name AS distribution_center_name,
            ii.product_category,
            COUNT(*) AS shipped_count
        FROM src.order_items oi
        JOIN src.inventory_items ii ON oi.inventory_item_id = ii.id
        JOIN src.distribution_centres dc ON ii.product_distribution_center_id = dc.id
        WHERE oi.shipped_at IS NOT NULL
          AND ii.product_category IN (SELECT product_category FROM top_categories)
        GROUP BY dc.name, ii.product_category
        ORDER BY shipped_count DESC
    '''
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['distribution_center_name', 'product_category', 'shipped_count'])
        if df.empty:
            st.write('No data available for the selected query.')
            return
        heatmap_data = df.pivot(index='distribution_center_name', columns='product_category', values='shipped_count').fillna(0)
        fig = px.imshow(
            heatmap_data,
            color_continuous_scale='Blues',
            aspect='auto'
        )
        fig.update_layout(
            showlegend=False,
            xaxis=dict(showticklabels=False),
            yaxis_title='Distribution Center',
            xaxis_title='Product Category',
            title=None
        )
        st.subheader('Distribution Centers for Top Categories')
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f'Error: {e}')


# indicator

# What is the total number of units sold across all categories?

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def total_units_sold_indicator():
    sql_query = """
        SELECT COALESCE(SUM(num_of_item), 0) AS total_units
        FROM src.orders
        WHERE status ILIKE '%delivered%'
    """
    try:
        db_connector = st.session_state['db_connector']
        result = db_connector.execute_query(sql_query)
        df = pd.DataFrame(result)
        total_units = int(df['total_units'].iloc[0]) if not df.empty else 0
        st.subheader('Total Units')
        fig = go.Figure(go.Indicator(
            mode = "number",
            value = total_units,
            number = {'font': {'size': 60}}
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


# indicator

# What is the total sales revenue generated by the top 10 categories?

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def total_revenue_top_10_categories():
    sql_query = """
        SELECT SUM(category_revenue) AS total_revenue
        FROM (
            SELECT ii.product_category, SUM(oi.sale_price) AS category_revenue
            FROM src.order_items oi
            JOIN src.inventory_items ii ON oi.inventory_item_id = ii.id
            WHERE oi.sale_price IS NOT NULL
            GROUP BY ii.product_category
            ORDER BY category_revenue DESC
            LIMIT 10
        ) AS top_categories
    """
    try:
        db_connector = st.session_state['db_connector']
        df = db_connector.execute_query(sql_query)
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


columns = 3
col1, col2,  = st.columns(2)
with col1:
	total_units_sold_indicator()
with col2:
	total_revenue_top_10_categories()
col1, col2, col3,  = st.columns(columns)
with col1:
	top_10_categories_by_units_sold()
with col2:
	sales_revenue_by_top_10_categories()
with col3:
	average_sale_price_by_category()
col4, col5, col6,  = st.columns(columns)
with col4:
	top_brands_in_leading_categories()
with col5:
	distribution_centers_top_categories_heatmap()
