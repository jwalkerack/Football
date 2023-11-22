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
cursor.execute("""
    SELECT GS.id, GS.HomePossession,T.teamName,W.gameWeekName
    FROM GameStats AS GS
    LEFT JOIN Games AS G ON GS.gameId = G.id
    LEFT JOIN Teams AS T ON CAST(G.homeTeam AS UNSIGNED) = T.id
    LEFT JOIN GameWeeks AS W ON G.gameWeek = W.id
    WHERE GS.HomePossession > 60;
""")
data = cursor.fetchall()


for item in data:
    print (item)
cursor.close()
cnx.close()