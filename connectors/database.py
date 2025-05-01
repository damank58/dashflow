from sqlalchemy import create_engine, text, URL
from sqlalchemy.exc import SQLAlchemyError

# load_dotenv()
"""
url = URL.create(
    drivername="postgresql+psycopg2",
    password=os.getenv("DB_PWD"),
    username=os.getenv("DB_USER"),
    host=os.getenv("DB_HOST"),
    database=os.getenv("DATABASE"),
    port=os.getenv("DB_PORT")
)

# SQLAlchemy Engine for direct pandas queries
engine = create_engine(url)
"""


def execute_query(sql_query):
    try:
        connection = engine.connect()
        result_proxy = connection.execute(text(sql_query))
        if result_proxy.returns_rows:
            results = result_proxy.fetchall()
        else:
            results = "Query executed successfully (no return data)."
        connection.close()
        return results
    except Exception as e:
        return f"Error executing query: {e}"


def get_schema():
    sql_query = '''SELECT table_schema, table_name, column_name, data_type 
                FROM information_schema.columns cols
                WHERE table_schema = 'src'
                  AND table_name NOT IN (
                    SELECT c.relname
                    FROM pg_inherits i
                    JOIN pg_class c ON i.inhrelid = c.oid
                    JOIN pg_namespace n ON c.relnamespace = n.oid
                    WHERE n.nspname = 'src'
                  )
                ORDER BY table_name;'''
    out = execute_query(sql_query)
    schema = ''
    for table in out:
        schema += f"\n{table[0]}.{table[1]}.{table[2]}, {table[3]};"
    return schema


def create_conn(db_url, db_type):
    try:
        engine = create_engine(db_url)
        with engine.connect() as conn:
            # Run a version query depending on DB type
            version_query = "SELECT version();" if db_type != "SQLite" else "SELECT sqlite_version();"
            result = conn.execute(text(version_query))
            version = result.scalar()
            return f"Connected to {db_type}!\nVersion: {version}"
    except SQLAlchemyError as e:
        return f"Connection failed: {e}"


class DatabaseConnection(object):

    def __init__(self, db_creds, db_type):
        self.db_type = db_type
        self.engine = self._get_engine(db_creds)

    def _get_engine(self, db_creds):
        if self.db_type == 'SQLite':
            db_url = db_creds['db_url']
        else:
            db_url = URL.create(
                drivername=db_creds['drivername'],
                password=db_creds['password'],
                username=db_creds['username'],
                host=db_creds['host'],
                database=db_creds['database'],
                port=db_creds['port']
            )
        engine = create_engine(db_url)
        return engine

    def execute_query(self, sql_query):
        try:
            with self.engine.connect() as conn:
                result_proxy = conn.execute(text(sql_query))
                if result_proxy.returns_rows:
                    results = result_proxy.fetchall()
                else:
                    results = "Query executed successfully (no return data)."
            # cls.conn.close()
            return results
        except Exception as e:
            return f"Error executing query: {e}"

    def get_schema(self):
        pg_query = '''SELECT table_schema, table_name, column_name, data_type 
                        FROM information_schema.columns cols
                        WHERE table_schema = 'src'
                          AND table_name NOT IN (
                            SELECT c.relname
                            FROM pg_inherits i
                            JOIN pg_class c ON i.inhrelid = c.oid
                            JOIN pg_namespace n ON c.relnamespace = n.oid
                            WHERE n.nspname = 'src'
                          )
                        ORDER BY table_name;'''
        if self.db_type == 'PostgreSQL':
            schema_query = pg_query

        else:
            raise Exception('Invalid Database Type')

        out = self.execute_query(schema_query)
        schema = ''
        for table in out:
            schema += f"\n{table[0]}.{table[1]}.{table[2]}, {table[3]};"
        return schema
