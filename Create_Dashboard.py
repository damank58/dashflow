import streamlit as st
from graph_agent import DashAgent
from connectors.database import DatabaseConnection

st.set_page_config(page_title="DashFlow", layout="wide")

# Initialize session state
if 'user_input' not in st.session_state:
    st.session_state['user_input'] = ''
if 'run_dashboard' not in st.session_state:
    st.session_state['run_dashboard'] = False
if 'db_connector' not in st.session_state:
    st.session_state['db_connector'] = None

st.title("📊 DashFlow")
st.markdown("<div style='height: 20vh;'></div>", unsafe_allow_html=True)


st.sidebar.subheader("Database Credentials")

if not st.session_state['db_connector']:
    # Sidebar selection for DB type
    db_type = st.sidebar.selectbox("Select Database Type", ("SQLite", "PostgreSQL", "MySQL"))

    # Input fields based on DB type
    if db_type == "SQLite":
        file_path = st.sidebar.text_input("SQLite DB File Path", value="example.db")
        db_creds = {'db_url': f"sqlite:///{file_path}"}
    else:
        host = st.sidebar.text_input("Host", value="localhost")
        port = st.sidebar.text_input("Port", value="5432" if db_type == "PostgreSQL" else "3306")
        database = st.sidebar.text_input("Database Name", value="ecommerce")
        user = st.sidebar.text_input("Username", value="postgres")
        password = st.sidebar.text_input("Password", type="password")

        if db_type == "PostgreSQL":
            db_creds = {'drivername': 'postgresql+psycopg2',
                        'host': host,
                        'port': 5432,
                        'database': database,
                        'username': user,
                        'password': password}
        elif db_type == "MySQL":
            db_creds = {'drivername': 'mysql+pymysql',
                        'host': host,
                        'port': 3306,
                        'database': database,
                        'username': user,
                        'password': password}
        else:
            db_creds = {}

    # Connect and test
    if db_creds and st.sidebar.button("Connect"):
        db_connector = DatabaseConnection(db_creds=db_creds, db_type=db_type)
        st.session_state['db_connector'] = db_connector
        st.sidebar.success('Connected!')
else:
    st.sidebar.success("Connected!")

with st.container():
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        st.header("What dashboard would you like to build today?")
    st.session_state['user_input'] = st.text_area(label="Enter here..", value="Create a dashboard ", height=100,
                                                  label_visibility='hidden')

if st.session_state['db_connector'] and st.button("Get Dashboard"):
    db_connector = st.session_state['db_connector']
    schema = db_connector.get_schema()
    st.session_state['run_dashboard'] = True
    with st.spinner("Designing your dashboard...", show_time=True):
        DashAgent(schema).create_dashboard(user_prompt=st.session_state['user_input'])
    st.success("Dashboard is ready! You can see a new page on your sidebar panel.")
    st.rerun()

if not st.session_state.get('run_dashboard'):
    st.stop()

if not st.session_state['db_connector']:
    st.error("Database not connected. Please connect first.")
    st.stop()
