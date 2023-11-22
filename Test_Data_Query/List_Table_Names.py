import mysql.connector

# Database configuration
config = {
    'user': 'root',
    'password': 'example',  # Use your root password here
    'host': 'localhost',
    'port': 3307,  # The new port you're using for MariaDB
}

# Establish a database connection
cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

# Select the database
cursor.execute("USE Football;")

# Execute a query to retrieve tables
cursor.execute("SHOW TABLES;")

# Fetch all the results
tables = cursor.fetchall()

# Output the tables
for (table_name,) in tables:
    print(table_name)

# Close the cursor and connection
cursor.close()
cnx.close()