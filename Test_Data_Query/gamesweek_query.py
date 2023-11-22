import mysql.connector

# Database configuration
config = {
    'user': 'root',
    'password': 'example',  # Use your root password here
    'host': 'localhost',
    'port': 3307,
}

# Establish a database connection
cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()
# Select the database
cursor.execute("USE Football;")
# Query to count home games for each team
cursor.execute("""
SELECT gameWeek ,count(*)
FROM Games
GROUP BY gameWeek;
""")
home_games = cursor.fetchall()

Data = []

for g in home_games:
    row = [g[0] , "GameWeek-" + str(g[0]) , 0]
    Data.append(row)

import pandas as pd

df = pd.DataFrame(Data, columns=['id', 'gameWeekName','HasBeenPlayed'])

print (df)