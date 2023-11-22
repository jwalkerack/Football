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

truncate_query = "TRUNCATE TABLE RunningTable;"
cursor.execute(truncate_query)

# Fetch the list of all tables in the Football database
cursor.execute("""
INSERT INTO RunningTable (POS, TeamID, TeamName, Played, Won, Lost, Drawn, GoalsFor, GoalsAgaisnt, GoalDifference,Points)
SELECT 
ROW_NUMBER() OVER (ORDER BY Points DESC ,Wins desc ,GoalDifference desc) AS Pos,
    T.id as TeamId,
    T.TeamName as TeamName,
    SUM(sub.Played) AS Played, 
    SUM(sub.Wins) AS Won,
    SUM(sub.Lost) AS Lost, 
    SUM(sub.Draws) AS Drawn, 
    SUM(sub.GoalsScored) AS GoalsFor, 
    SUM(sub.GoalsConceded) AS GoalsAgaisnt,
    (SUM(sub.GoalsScored) - SUM(sub.GoalsConceded)) AS GoalDifference,
    (SUM(sub.Wins) * 3 + SUM(sub.Draws)) AS Points

FROM 
    (
        SELECT G.homeTeam as TeamId, 
            COUNT(*) as Played, 
            COUNT(CASE WHEN GS.matchOutcome = 'H' THEN 1 END) AS Wins, 
            COUNT(CASE WHEN GS.matchOutcome = 'D' THEN 1 END) AS Draws,
            COUNT(CASE WHEN GS.matchOutcome = 'A' THEN 1 END) AS Lost,
            SUM(GS.HomeScore) AS GoalsScored, 
            SUM(GS.AwayScore) AS GoalsConceded
        FROM GameStats AS GS
        LEFT JOIN Games as G ON GS.gameId = G.id
        GROUP BY G.homeTeam

        UNION ALL

        SELECT G.awayTeam as TeamId, 
            COUNT(*) as Played, 
            COUNT(CASE WHEN GS.matchOutcome = 'A' THEN 1 END) AS Wins, 
            COUNT(CASE WHEN GS.matchOutcome = 'D' THEN 1 END) AS Draws,
            COUNT(CASE WHEN GS.matchOutcome = 'H' THEN 1 END) AS Lost,
            SUM(GS.AwayScore) AS GoalsScored, 
            SUM(GS.HomeScore) AS GoalsConceded
        FROM GameStats AS GS
        LEFT JOIN Games as G ON GS.gameId = G.id
        GROUP BY G.awayTeam
    ) AS sub
LEFT JOIN Teams AS T ON sub.TeamId = T.id
GROUP BY T.TeamName
ORDER BY Points DESC ,Wins desc ,GoalDifference desc ;""")
cnx.commit()

# Optionally, fetch and print the new data from RunningTable
cursor.execute("SELECT * FROM RunningTable;")
data = cursor.fetchall()

for item in data:
    print(item)

# Close the cursor and connection
cursor.close()
cnx.close()
