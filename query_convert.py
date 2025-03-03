import re

def convert_mysql_to_sybase(query):
    # Remove semicolon if present at the end (Sybase doesn't need it)
    query = query.rstrip(';')
    
    # Convert AUTO_INCREMENT to IDENTITY
    query = re.sub(r'\bAUTO_INCREMENT\b', 'IDENTITY', query)

    # Convert LIMIT to TOP (for simple cases)
    query = re.sub(r'LIMIT (\d+)', r'TOP \1', query)

    # Convert CONCAT() to + for string concatenation
    query = re.sub(r'CONCAT\((.*?)\)', r'\1', query)  # remove CONCAT
    query = query.replace(',', ' +')  # replace commas with plus for concatenation

    # Handle other MySQL-Specific functions (like NOW, CURDATE, etc.)
    query = query.replace("CURDATE()", "CURRENT_DATE")
    query = query.replace("NOW()", "GETDATE()")
    
    # Handle case for OFFSET (Sybase doesn't have OFFSET directly)
    query = re.sub(r'OFFSET (\d+)', '', query)  # Sybase doesn't support OFFSET directly, remove it.
    
    # Return the converted query (no semicolon at the end)
    return query

def convert_sybase_to_mysql(query):
    # Convert TOP to LIMIT for basic queries
    query = re.sub(r'\sTOP\s(\d+)', r'LIMIT \1', query)

    # Convert TOP with OFFSET (if present)
    query = re.sub(r'\sTOP\s(\d+)\s*OFFSET\s*(\d+)', r'LIMIT \2, \1', query)

    # Convert string concatenation from + to CONCAT()
    query = re.sub(r'(\w+)\s*\+\s*(\w+)', r'CONCAT(\1, \2)', query)

    # Convert GETDATE() to NOW()
    query = query.replace("GETDATE()", "NOW()")

    # Convert CURRENT_DATE to CURDATE()
    query = query.replace("CURRENT_DATE", "CURDATE()")
    
    return query

    # Return the converted query with a semicolon
    return query
def convert_file_to_mysql(input_file, output_file):
    """ Reads a Sybase SQL file, converts queries, and writes them to a MySQL SQL file. """
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            converted_line = convert_sybase_to_mysql(line)
            if converted_line:
                outfile.write(converted_line.strip() + "\n")

def convert_file_to_sybase(input_file, output_file):
    """ Reads a MySQL SQL file, converts queries, and writes them to a Sybase SQL file. """
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            converted_line = convert_mysql_to_sybase(line)
            if converted_line:
                outfile.write(converted_line.strip() + "\n")
