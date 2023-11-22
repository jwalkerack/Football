import mysql.connector

# Database configuration
config = {
    'user': 'root',
    'password': 'example',
    'host': 'localhost',
    'port': 3307,
    'database': 'Football',
}

# Establish a database connection
cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

# Query to count home games for each team
cursor.execute("""
SELECT HomeTeam, COUNT(*) as HomeGames
FROM Games
GROUP BY HomeTeam;
""")
home_games = cursor.fetchall()

# Query to count away games for each team
cursor.execute("""
SELECT AwayTeam, COUNT(*) as AwayGames
FROM Games
GROUP BY AwayTeam;
""")
away_games = cursor.fetchall()

# Close the cursor and connection
cursor.close()
cnx.close()

# Convert the results to dictionaries for easy lookup
home_games_count = {team: count for team, count in home_games}
away_games_count = {team: count for team, count in away_games}

# You can print the results or work with them further here.
print("Home Games Count:")
for team, count in home_games_count.items():
    print(f"{team}: {count}")

print("\nAway Games Count:")
for team, count in away_games_count.items():
    print(f"{team}: {count}")

