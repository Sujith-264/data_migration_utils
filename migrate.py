import pyodbc
import mysql.connector
import data_migrate as dm

# Database connection details
SYBASE_CONN_STR = dm.sybase_connection()
MYSQL_CONN_STR = dm.mysql_connection()

def get_schema_from_mysql():
    """Extracts schema details from MySQL."""
    conn = mysql.connector.connect(MYSQL_CONN_STR)
    cursor = conn.cursor()
    
    cursor.execute("SHOW TABLES;")
    schema_data = cursor.fetchall()
    
    conn.close()
    return schema_data

def get_schema_from_sybase():
    """Extracts schema details from Sybase."""
    conn = pyodbc.connect(SYBASE_CONN_STR)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sysobjects WHERE type = 'U';")
    schema_data = cursor.fetchall()
    
    conn.close()
    return schema_data

def convert_mysql_to_sybase(mysql_schema):
    """Converts MySQL schema to Sybase-compatible statements."""
    converted_statements = []
    
    for obj in mysql_schema:
        name = obj[0]
        converted_statements.append(f"CREATE TABLE {name} (id INT PRIMARY KEY);")
    
    return converted_statements

def convert_sybase_to_mysql(sybase_schema):
    """Converts Sybase schema to MySQL-compatible statements."""
    converted_statements = []
    
    for obj in sybase_schema:
        name = obj[0]
        converted_statements.append(f"CREATE TABLE {name} (id INT PRIMARY KEY);")
    
    return converted_statements

def execute_statements_on_mysql(statements):
    """Executes the converted schema statements on MySQL."""
    conn = mysql.connector.connect(**MYSQL_CONN_DETAILS)
    cursor = conn.cursor()
    
    for stmt in statements:
        cursor.execute(stmt)
    
    conn.commit()
    conn.close()

def execute_statements_on_sybase(statements):
    """Executes the converted schema statements on Sybase."""
    conn = pyodbc.connect(SYBASE_CONN_STR)
    cursor = conn.cursor()
    
    for stmt in statements:
        cursor.execute(stmt)
    
    conn.commit()
    conn.close()

def migrate_mysql_to_sybase():
    """Complete process: Extract from MySQL, Convert, Execute on Sybase."""
    schema = get_schema_from_mysql()
    sybase_statements = convert_mysql_to_sybase(schema)
    execute_statements_on_sybase(sybase_statements)
    print("Schema migration from MySQL to Sybase completed!")

def migrate_sybase_to_mysql():
    """Complete process: Extract from Sybase, Convert, Execute on MySQL."""
    schema = get_schema_from_sybase()
    mysql_statements = convert_sybase_to_mysql(schema)
    execute_statements_on_mysql(mysql_statements)
    print("Schema migration from Sybase to MySQL completed!")
