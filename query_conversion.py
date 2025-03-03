import re

def convert_mysql_to_sybase(mysql_sql):
    replacements = [
        # Data Types
        (r'INT AUTO_INCREMENT', 'INT IDENTITY'),
        (r'DATETIME', 'SMALLDATETIME'),
        (r'TEXT', 'VARCHAR(MAX)'),
        (r'LONGTEXT', 'TEXT'),
        (r'IFNULL\((.*?), (.*?)\)', r'ISNULL(\1, \2)'),
        (r'BOOLEAN', 'BIT'),
        (r'CHAR\(36\)', 'UNIQUEIDENTIFIER'),

        # String Concatenation
        (r'CONCAT\((.*?)\)', r'\1'),  # Assuming MySQL CONCAT needs to be rewritten manually
        
        # LIMIT to TOP
        (r'SELECT (.*?) FROM (.*?) LIMIT (\d+)', r'SELECT TOP \3 \1 FROM \2'),
        
        # NOW() to GETDATE()
        (r'NOW\(\)', 'GETDATE()'),
        (r'CURDATE\(\)', 'CURRENT_DATE'),
        
        # CASE statement remains mostly the same but check for minor changes
        
        # JOIN syntax
        (r'LEFT JOIN', 'LEFT OUTER JOIN'),
        (r'RIGHT JOIN', 'RIGHT OUTER JOIN'),

        # NULL Comparison
        (r'WHERE (.*?) = NULL', r'WHERE \1 IS NULL'),

        # Temporary Table Handling
        (r'CREATE TEMPORARY TABLE (.*?) AS SELECT', r'SELECT INTO #\1 FROM'),
        
        # Triggers
        (r'DELIMITER //', ''),  
        #(r'CREATE TRIGGER (\w+) \r\n(BEFORE|AFTER) UPDATE ON (\w+) \r\nFOR EACH ROW', r'CREATE TRIGGER \1 ON \3 FOR UPDATE AS'),
        (r'CREATE TRIGGER (\w+)\s+(BEFORE|AFTER) UPDATE ON (\w+)\s+FOR EACH ROW', r'CREATE TRIGGER \1 ON \3 FOR UPDATE AS'),
        (r'SET NEW\.(\w+) = NOW\(\);', r'UPDATE inserted SET \1 = GETDATE();'),  
        (r'END', 'END'),  
        (r'//',''),
        (r'DELIMITER ;', ''),
        
        
        # DELETE with LIMIT
        (r'DELETE FROM (.*?) WHERE (.*?) LIMIT (\d+)', r'DELETE TOP (\3) FROM \1 WHERE \2'),
        
        
        
        (r'DELIMITER //', ''),  
        (r'CREATE PROCEDURE (\w+)\((.*?)\)\s+BEGIN', r'CREATE PROCEDURE \1(\2) AS'),  
        (r'\bIN (\w+) (\w+)', r'@\1 \2'),  
        (r'LEAVE', 'RETURN'),  
        (r'END //', 'END;'),  
        (r'DELIMITER', ''),
        
        # Views
        (r'CREATE VIEW (.*?) AS', r'CREATE VIEW \1 AS'),
        
        # Indexes
        (r'CREATE INDEX (.*?) ON (.*?)\((.*?)\);', r'CREATE INDEX \1 ON \2(\3);'),
    ]
    
    # Remove semicolons at the end of each query
    mysql_sql = re.sub(r';\s*$', '', mysql_sql, flags=re.MULTILINE)
    
    for pattern, replacement in replacements:
        mysql_sql = re.sub(pattern, replacement, mysql_sql, flags=re.IGNORECASE)
    
    return mysql_sql
def convert_sybase_to_mysql(sybase_sql):
    replacements = [
        # Data Types
        (r'INT IDENTITY', 'INT AUTO_INCREMENT'),
        (r'SMALLDATETIME', 'DATETIME'),
        (r'VARCHAR\(MAX\)', 'TEXT'),
        (r'TEXT', 'LONGTEXT'),
        (r'ISNULL\((.*?), (.*?)\)', r'IFNULL(\1, \2)'),
        (r'BIT', 'BOOLEAN'),
        (r'UNIQUEIDENTIFIER', 'CHAR(36)'),

        # String Concatenation (Fixing + operator for MySQL)
        (r'\b(\w+) \+ (\w+)\b', r'CONCAT(\1, " ", \2)'),
        (r'\b(\w+) \+ \s" "\s\+ (\w+)\b', r'CONCAT(\1, " ", \2)'),
        
        # TOP to LIMIT (Fixing misplaced LIMIT position)
        # (r'SELECT TOP (\d+) (.*?) FROM (.*?)', r'SELECT \2 FROM \3 LIMIT \1'),
        (r'SELECT TOP (\d+) (.*?) FROM (\w+)(.*?)', r'SELECT \2 FROM \3\4 LIMIT \1'),

        
        # GETDATE() to NOW()
        (r'GETDATE\(\)', 'NOW()'),
        (r'CURRENT_DATE', 'CURDATE()'),
        
        # JOIN syntax
        (r'LEFT OUTER JOIN', 'LEFT JOIN'),
        (r'RIGHT OUTER JOIN', 'RIGHT JOIN'),

        # NULL Comparison
        (r'WHERE (.*?) IS NULL', r'WHERE \1 IS NULL'),

        # Temporary Table Handling
        (r'SELECT INTO #(.*?) FROM', r'CREATE TEMPORARY TABLE \1 AS SELECT'),
        
        # Triggers
        (r'CREATE TRIGGER (.*?) ON (.*?) FOR UPDATE AS', r'CREATE TRIGGER \1 AFTER UPDATE ON \2 FOR EACH ROW'),
        
        # DELETE with TOP
        (r'DELETE TOP \((\d+)\) FROM (.*?) WHERE (.*?)', r'DELETE FROM \2 WHERE \3 LIMIT \1'),
        
        (r'CREATE PROCEDURE (\w+) \((.*?)\) AS', r'DELIMITER // \n\rCREATE PROCEDURE \1(\2)'),  
        (r'@(\w+) (\w+)', r'IN \1 \2'),  
        (r'RETURN', 'LEAVE'),  
        (r'END', r'END //\nDELIMITER ;'),  
        (r'CREATE PROCEDURE (\w+)', r'CREATE PROCEDURE \1'),
        
        # Views
        (r'CREATE VIEW (.*?) AS', r'CREATE VIEW \1 AS'),
        
        # Indexes
        (r'CREATE INDEX (.*?) ON (.*?)\((.*?)\);', r'CREATE INDEX \1 ON \2(\3);'),
    ]
    
    # Remove non-printable characters (fixing unexpected symbols)
    sybase_sql = re.sub(r'[^\x20-\x7E\n]', '', sybase_sql)
    
    for pattern, replacement in replacements:
        sybase_sql = re.sub(pattern, replacement, sybase_sql, flags=re.IGNORECASE)
    
    # Ensure semicolons are correctly placed at the end of statements
    sybase_sql = re.sub(r'(\n|^)(SELECT|UPDATE|DELETE|INSERT|CREATE|DROP|ALTER)(.*?)(\n|$)', r'\1\2\3;', sybase_sql, flags=re.IGNORECASE)
    
    return sybase_sql

# Read MySQL SQL file and convert
input_file_for_mysql_to_sybase = "./sql_files/mysql_queries.sql"
output_file_for_mysql_to_sybase = "./sql_files/converted_sybase_queries.sql"
input_file_for_sybase_to_mysql = "./sql_files/sybase_queries.sql"
output_file_for_sybase_to_mysql = "./sql_files/converted_mysql_queries.sql"


def convert_file_to_mysql(input_file_for_sybase_to_mysql, output_file_for_sybase_to_mysql):
    with open(input_file_for_sybase_to_mysql, "r") as f:
        sybase_sql = f.read()

    mysql_sql = convert_sybase_to_mysql(sybase_sql)

    with open(output_file_for_sybase_to_mysql, "w") as f:
        f.write(mysql_sql)

    print(f"Conversion complete. MySQL SQL file saved as {output_file_for_sybase_to_mysql}")

def convert_file_to_sybase(input_file_for_mysql_to_sybase, output_file_for_mysql_to_sybase):
    with open(input_file_for_mysql_to_sybase, "r") as f:
        mysql_sql = f.read()

    sybase_sql = convert_mysql_to_sybase(mysql_sql)

    with open(output_file_for_mysql_to_sybase, "w") as f:
        f.write(sybase_sql)

    print(f"Conversion complete. Sybase SQL file saved as {output_file_for_mysql_to_sybase}")