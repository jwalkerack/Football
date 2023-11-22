import mysql.connector

# Database configuration
config = {
    'user': 'root',
    'password': 'example',  # Replace with your root password
    'host': 'localhost',
    'port': 3307,  # Replace with the correct port if needed
    'database': 'Football',  # The database you want to connect to
}

# Establish a database connection
cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

# Fetch the list of all tables in the Football database
cursor.execute("SHOW TABLES;")
tables = cursor.fetchall()

# Iterate over the tables and display the first 20 rows from each
for (table_name,) in tables:
    print(f"First 20 rows from table '{table_name}':")
    try:
        cursor.execute(f"SELECT * FROM `{table_name}` LIMIT 20;")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    print("-" * 40)  # Separator for readability

# Close the cursor and connection
cursor.close()
cnx.close()