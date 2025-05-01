import streamlit as st


st.title("Leggings Sales Performance Analysis 2022")

# line chart

# What were the monthly sales trends for Leggings in 2022?

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def monthly_leggings_sales_trend_2022():
    sql_query = '''
        SELECT 
            DATE_TRUNC('month', oi.created_at) AS month,
            SUM(oi.sale_price) AS total_sales
        FROM src.order_items oi
        JOIN src.inventory_items ii ON oi.inventory_item_id = ii.id
        WHERE ii.product_category ILIKE '%Leggings%'
          AND oi.created_at >= '2022-01-01'
          AND oi.created_at < '2023-01-01'
        GROUP BY month
        ORDER BY month
    '''
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['month', 'total_sales'])
        st.subheader('Monthly Leggings Sales Trend')
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['month'], y=df['total_sales'], mode='lines+markers', showlegend=False))
        fig.update_layout(xaxis=dict(showticklabels=False), yaxis_title='Total Sales ($)')
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading chart: {e}")


# bar chart

# Which distribution centres sold the most Leggings in 2022?

def sales_by_distribution_centre_leggings_2022():
    import streamlit as st
    import pandas as pd
    import plotly.graph_objects as go
    sql_query = '''
        SELECT dc.name AS distribution_centre, COUNT(oi.id) AS leggings_sold
        FROM src.order_items oi
        JOIN src.inventory_items ii ON oi.inventory_item_id = ii.id
        JOIN src.distribution_centres dc ON ii.product_distribution_center_id = dc.id
        WHERE ii.product_name ILIKE '%Leggings%'
          AND oi.created_at >= '2022-01-01' AND oi.created_at < '2023-01-01'
        GROUP BY dc.name
        ORDER BY leggings_sold DESC
        LIMIT 20
    '''
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['distribution_centre', 'leggings_sold'])
        st.subheader('Sales by Distribution Centre')
        fig = go.Figure(go.Bar(
            x=df['distribution_centre'],
            y=df['leggings_sold'],
            marker_color='indigo',
            showlegend=False
        ))
        fig.update_layout(
            xaxis=dict(showticklabels=False),
            yaxis_title='Leggings Sold',
            xaxis_title='Distribution Centre',
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading chart: {e}")


# choropleth map

# What was the geographic distribution of Leggings sales by state in 2022?

def leggings_sales_by_state_2022():
    import streamlit as st
    import pandas as pd
    import plotly.express as px
    sql_query = '''
        SELECT u.state AS state, COUNT(oi.id) AS leggings_sales
        FROM src.order_items oi
        JOIN src.inventory_items ii ON oi.inventory_item_id = ii.id
        JOIN src.products p ON ii.product_id = p.id
        JOIN src.orders o ON oi.order_id = o.order_id
        JOIN src.users u ON o.user_id = u.id
        WHERE p.name ILIKE '%legging%'
          AND oi.created_at >= '2022-01-01' AND oi.created_at < '2023-01-01'
        GROUP BY u.state
        ORDER BY leggings_sales DESC
    '''
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['state', 'leggings_sales'])
        st.subheader('Leggings Sales by State')
        fig = px.choropleth(
            df,
            locations='state',
            locationmode='USA-states',
            color='leggings_sales',
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
    except Exception as e:
        st.error(f"Error loading data or rendering chart: {e}")


# pie chart

# How did Leggings sales vary by customer gender in 2022?

def leggings_sales_by_gender_2022():
    import streamlit as st
    import pandas as pd
    import plotly.express as px
    sql_query = '''
        SELECT o.gender AS customer_gender, SUM(oi.sale_price) AS total_sales
        FROM src.order_items oi
        JOIN src.orders o ON oi.order_id = o.order_id
        JOIN src.products p ON oi.product_id = p.id
        WHERE p.name ILIKE '%leggings%'
          AND o.created_at >= '2022-01-01' AND o.created_at < '2023-01-01'
          AND o.gender IS NOT NULL
        GROUP BY o.gender
        ORDER BY total_sales DESC
    '''
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['customer_gender', 'total_sales'])
        st.subheader('Sales by Customer Gender')
        fig = px.pie(df, names='customer_gender', values='total_sales')
        fig.update_layout(showlegend=False)
        fig.update_xaxes(showticklabels=False)
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading chart: {e}")


# bar chart

# What was the return rate for Leggings orders in 2022?

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def leggings_return_rate_2022():
    sql_query = '''
        SELECT 
            'Leggings' AS product_category,
            COUNT(CASE WHEN oi.returned_at IS NOT NULL THEN 1 END)::float / NULLIF(COUNT(oi.id),0) AS return_rate
        FROM src.order_items oi
        JOIN src.inventory_items ii ON oi.inventory_item_id = ii.id
        JOIN src.products p ON oi.product_id = p.id
        WHERE (ii.product_category ILIKE '%Leggings%' OR p.category ILIKE '%Leggings%' OR ii.product_name ILIKE '%Leggings%' OR p.name ILIKE '%Leggings%')
          AND oi.created_at >= '2022-01-01' AND oi.created_at < '2023-01-01'
    '''
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['product_category', 'return_rate'])
        st.subheader('Leggings Return Rate')
        fig = go.Figure(go.Bar(
            x=df['product_category'],
            y=df['return_rate'],
            showlegend=False
        ))
        fig.update_layout(
            xaxis=dict(showticklabels=False),
            yaxis_title='Return Rate',
            title=None
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error: {e}")


# bar chart

# Which Leggings brands had the highest sales in 2022?

def leggings_brand_sales_2022():
    sql_query = '''
        SELECT 
            ii.product_brand AS brand, 
            SUM(oi.sale_price) AS total_sales
        FROM src.order_items oi
        JOIN src.inventory_items ii ON oi.inventory_item_id = ii.id
        WHERE ii.product_category ILIKE '%Leggings%'
          AND oi.created_at >= '2022-01-01' AND oi.created_at < '2023-01-01'
          AND oi.status ILIKE '%delivered%'
        GROUP BY ii.product_brand
        ORDER BY total_sales DESC
        LIMIT 10
    '''
    import streamlit as st
    import pandas as pd
    import plotly.express as px
    try:
        db_connector = st.session_state['db_connector']
        records = db_connector.execute_query(sql_query)
        df = pd.DataFrame(records, columns=['brand', 'total_sales'])
        st.subheader('Sales by Leggings Brand')
        fig = px.bar(df, x='brand', y='total_sales')
        fig.update_layout(showlegend=False, xaxis=dict(showticklabels=False))
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading data: {e}")


# indicator

# What was the total revenue from Leggings sales in 2022?

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def leggings_revenue_2022_indicator():
    sql_query = '''
        SELECT COALESCE(SUM(oi.sale_price), 0) AS total_revenue
        FROM src.order_items oi
        JOIN src.inventory_items ii ON oi.inventory_item_id = ii.id
        WHERE ii.product_name ILIKE '%leggings%'
          AND oi.created_at >= '2022-01-01' AND oi.created_at < '2023-01-01'
    '''
    try:
        db_connector = st.session_state['db_connector']
        result = db_connector.execute_query(sql_query)
        df = pd.DataFrame(result)
        total_revenue = df['total_revenue'].iloc[0] if not df.empty else 0
        st.subheader('Revenue')
        fig = go.Figure(go.Indicator(
            mode = 'number',
            value = total_revenue,
            number = {'prefix': '$', 'valueformat': ',.2f'},
            title = {'text': ''}
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


# indicator

# How many Leggings units were sold in 2022?

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def leggings_units_sold_2022():
    sql_query = """
        SELECT COUNT(*) AS units_sold
        FROM src.inventory_items
        WHERE product_name ILIKE '%Leggings%'
          AND sold_at >= '2022-01-01' AND sold_at < '2023-01-01'
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
	leggings_revenue_2022_indicator()
with col2:
	leggings_units_sold_2022()
col1, col2, col3,  = st.columns(columns)
with col1:
	monthly_leggings_sales_trend_2022()
with col2:
	sales_by_distribution_centre_leggings_2022()
with col3:
	leggings_sales_by_state_2022()
col4, col5, col6,  = st.columns(columns)
with col4:
	leggings_sales_by_gender_2022()
with col5:
	leggings_return_rate_2022()
with col6:
	leggings_brand_sales_2022()
