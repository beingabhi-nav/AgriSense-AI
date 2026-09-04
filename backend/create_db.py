import pymysql

try:
    # Connect to DBngin MySQL server without a password
    connection = pymysql.connect(host='127.0.0.1', user='root', password='')
    cursor = connection.cursor()
    
    # Create the database for your project
    cursor.execute("CREATE DATABASE IF NOT EXISTS agrisense_db;")
    print("Success! agrisense_db created successfully.")
    
    cursor.close()
    connection.close()
except Exception as e:
    print(f"Error: {e}")