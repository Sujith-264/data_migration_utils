import pyodbc
import mysql.connector
import pandas as pd
import configparser as cp
from contextlib import contextmanager

# Context manager for Sybase connection
@contextmanager
def sybase_connection():
   
    config = cp.ConfigParser()
    config.read("./config/Connections.ini")

    db_server = config.get("sybase", "server")
    db_port = int(config.get("sybase", "port"))
    db_name = config.get("sybase", "database")
    db_id = config.get("sybase", "uid")
    db_pwd = config.get("sybase", "pwd")
    # Connect to Sybase (adjust with your details)
    conn_sybase = pyodbc.connect(
    'DRIVER={Adaptive Server Enterprise};'
    f'SERVER={db_server};'
    f'PORT={db_port};'
    f'DATABASE={db_name};'  
    f'UID={db_id};'
    f'PWD={db_pwd}')
    try:
        yield conn_sybase
    finally:
        conn_sybase.close()

# Context manager for MySQL connection
@contextmanager
def mysql_connection():
    
    config = cp.ConfigParser()
    config.read("./config/Connections.ini")
    db_host = config.get("mysql","host")
    db_id = config.get("mysql","user")
    db_pwd = config.get("mysql","password")
    db_name = config.get("mysql","database")
    try:
        conn_mysql = mysql.connector.connect(
            host=f"{db_host}",
            user=f"{db_id}",
            password=f"{db_pwd}",
            database=f"{db_name}"
        )
        yield conn_mysql
    except mysql.connector.Error as e:
        print(f"MySQL Connection Error: {e}")
        yield None
    finally:
        if 'conn_mysql' in locals() and conn_mysql:
            conn_mysql.close()

# Function to extract data from Sybase
def get_sybase_data():
    with sybase_connection() as conn_sybase:
        config = cp.ConfigParser()
        config.read("./config/Connections.ini")
        db_table = config.get("sybase","table_name")
        if not conn_sybase:
            return [], []

        try:
            cursor = conn_sybase.cursor()
            query = f"SELECT * FROM {db_table}"
            cursor.execute(query)
            
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]

            data_from_sybase = [list(row) for row in rows]
            return data_from_sybase, column_names
        except pyodbc.Error as e:
            print(f"Error fetching data from Sybase: {e}")
            return [], []

# Function to extract data from MySQL
def get_mysql_data():
    with mysql_connection() as conn_mysql:
        config = cp.ConfigParser()
        config.read("./config/Connections.ini")
        db_table = config.get("mysql","table_name")
        if not conn_mysql:
            return [], []

        try:
            cursor = conn_mysql.cursor()
            query = f"SELECT * FROM {db_table}"
            cursor.execute(query)
            
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]

            data_from_mysql = [list(row) for row in rows]
            return data_from_mysql, column_names
        except mysql.connector.Error as e:
            print(f"Error fetching data from MySQL: {e}")
            return [], []

# Function to insert data into MySQL
def insert_into_mysql(column_names, data_from_sybase):
    config = cp.ConfigParser()
    config.read("./config/Connections.ini")
    db_table = config.get("mysql","table_name")
    if not data_from_sybase:
        print("No data to insert into MySQL. Skipping...")
        return

    with mysql_connection() as conn_mysql:
        if not conn_mysql:
            return

        try:
            cursor = conn_mysql.cursor()
            cols = ", ".join(column_names)
            placeholders = ", ".join(["%s"] * len(column_names))
            insert_query = f"INSERT INTO {db_table} ({cols}) VALUES ({placeholders})"

            batch_size = 1000  # Insert in batches
            for i in range(0, len(data_from_sybase), batch_size):
                batch = data_from_sybase[i : i + batch_size]
                cursor.executemany(insert_query, batch)

            conn_mysql.commit()
            print(f"Inserted {len(data_from_sybase)} rows into MySQL successfully.")
        except mysql.connector.Error as e:
            print(f"Error inserting data into MySQL: {e}")

# Function to insert data into Sybase
def insert_into_sybase(column_names, data_from_mysql):
    config = cp.ConfigParser()
    config.read("./config/Connections.ini")
    db_table = config.get("sybase","table_name")
    if not data_from_mysql:
        print("No data to insert into Sybase. Skipping...")
        return

    with sybase_connection() as conn_sybase:
        if not conn_sybase:
            return

        try:
            cursor = conn_sybase.cursor()
            cols = ", ".join(column_names)
            placeholders = ", ".join(["?"] * len(column_names))  # Sybase uses "?" for placeholders
            insert_query = f"INSERT INTO {db_table} ({cols}) VALUES ({placeholders})"

            batch_size = 1000  # Insert in batches
            for i in range(0, len(data_from_mysql), batch_size):
                batch = data_from_mysql[i : i + batch_size]
                cursor.executemany(insert_query, batch)

            conn_sybase.commit()
            print(f"Inserted {len(data_from_mysql)} rows into Sybase successfully.")
        except pyodbc.Error as e:
            print(f"Error inserting data into Sybase: {e}")
