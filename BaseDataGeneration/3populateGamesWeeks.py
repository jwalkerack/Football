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
SELECT gameWeek
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

from sqlalchemy import create_engine

engine = create_engine('mysql+mysqlconnector://root:example@localhost:3307/Football')

try:
    df.to_sql(name='GameWeeks', con=engine, if_exists='append', index=False)
    print("Data successfully written to GameWeeks Table.")
except Exception as e:
    print(f"An error occurred: {e}")