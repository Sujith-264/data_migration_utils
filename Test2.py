import query_conversion as qc

def test1():
    input_sql_file = "./sql_files/mysql_queries.sql"   # Input MySQL SQL file
    output_sql_file = "./sql_files/converted_sybase_queries.sql"  # Output Sybase SQL file
    qc.convert_file_to_sybase(input_sql_file, output_sql_file)
    #print(f"Conversion completed! Sybase queries saved in {output_sql_file}")

def test2():
    input_sql_file = "./sql_files/sybase_queries.sql"   # Input Sybase SQL file
    output_sql_file =  "./sql_files/converted_mysql_queries.sql" # Output MySQL SQL file
    qc.convert_file_to_mysql(input_sql_file, output_sql_file)
    #print(f"Conversion completed! MySQL queries saved in {output_sql_file}")

if __name__== "__main__":
    test1()
    test2()