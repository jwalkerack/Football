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
SELECT * FROM Games WHERE gameWeek IN 
(
SELECT MIN(id) 
FROM GameWeeks 
WHERE HasBeenPlayed = 0)
""")
games = cursor.fetchall()
Data = []

from CreateGameStats import GenerateGameStates

Data = []

for g in games:
    row = GenerateGameStates(g[0])
    Data.append(row)

import pandas as pd

df = pd.DataFrame(Data, columns=[
    'gameId',
    'HomePossession',
    'HomeYellow',
    'HomeRed',
    'HomeShots',
    'HomeShotsOnTarget',
    'HomeTouches',
    'HomeTouchesInFinalThird',
    'AwayPossession',
    'AwayYellow',
    'AwayRed',
    'AwayShots',
    'AwayShotsOnTarget',
    'AwayTouches',
    'AwayTouchesInFinalThird',
    'HomeScore',
    'AwayScore',
    'MatchOutcome'
])

from sqlalchemy import create_engine

# Replace 'mysqlconnector' with 'pymysql' if you are using PyMySQL
# Make sure the username, password, host, and port are consistent with your Docker configuration
engine = create_engine('mysql+mysqlconnector://root:example@localhost:3307/Football')
df.to_sql(name='GameStats', con=engine, if_exists='append', index=False)

update_statement = """
UPDATE GameWeeks
SET HasBeenPlayed = 1
WHERE id = (SELECT MIN(id) FROM GameWeeks WHERE HasBeenPlayed = 0);
"""

try:
    # Execute the update statement
    cursor.execute(update_statement)
    cnx.commit()  # Commit the changes
    print(f"Updated HasBeenPlayed to 1 for the GameWeek with the minimum ID where HasBeenPlayed was 0.")
except mysql.connector.Error as err:
    print(f"Error: {err}")
    cnx.rollback()  # Rollback in case of error

# Close the cursor and connection
cursor.close()
cnx.close()
