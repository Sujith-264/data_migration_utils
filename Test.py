import data_migrate as dm

def migrate_sybase_to_mysql():
    # Step 1: Extract data from Sybase
    sybase_data, column_names = dm.get_sybase_data()
    
    if not sybase_data:
        print("No data extracted from Sybase. Exiting migration.")
        return
    
    print(f"Extracted {len(sybase_data)} rows from Sybase.")

    # Step 2: Insert data into MySQL
    dm.insert_into_mysql(column_names, sybase_data)
    print("Data migration from Sybase to MySQL completed successfully.")

def migrate_mysql_to_sybase():
    # Step 1: Extract data from Sybase
    mysql_data, column_names = dm.get_mysql_data()
    
    if not mysql_data:
        print("No data extracted from MySQL. Exiting migration.")
        return
    
    print(f"Extracted {len(mysql_data)} rows from Sybase.")

    # Step 2: Insert data into MySQL
    dm.insert_into_sybase(column_names, mysql_data)
    print("Data migration from MYSQL to Sybase completed successfully.")
# Run the migration
if __name__ == "__main__":
    migrate_sybase_to_mysql()