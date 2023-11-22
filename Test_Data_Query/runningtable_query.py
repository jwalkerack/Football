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



try:
    cursor.execute("""SELECT TeamName , max(ModifiedDate)
                   FROM RunningTable
                   GROUP BY TeamName ;""")
    x = cursor.fetchall()
except mysql.connector.Error as err:
    print(f"Error: {err}")

print ("Team", "TeamCount")
for item in x:
    print (item)

try:
    cursor.execute("""SELECT *
                   FROM RunningTable;""")
    y = cursor.fetchall()
except mysql.connector.Error as err:
    print(f"Error: {err}")

print ('\n')
for item in y:
    print (item)


cursor.close()
cnx.close()