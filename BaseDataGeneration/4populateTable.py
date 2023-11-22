from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
# Replace with your actual database connection string
engine = create_engine('mysql+mysqlconnector://root:example@localhost:3307/Football')

query = text("""
INSERT INTO RunningTable (Pos, TeamId, TeamName,Played, Won, Lost, Drawn, GoalsFor, GoalsAgaisnt, GoalDifference, Points)
SELECT 
    ROW_NUMBER() OVER (ORDER BY TeamName ASC) AS Pos,
    id as TeamId,
    TeamName,
    0 AS Played ,
    0 AS Won,
    0 AS Lost,
    0 AS Drawn,
    0 AS GoalsFor,
    0 AS GoalsAgaisnt,
    0 AS GoalDifference,
    0 AS Points
FROM 
    Teams;
""")

try:
    with engine.connect() as conn:
        conn.execute(query)
        conn.commit()  # Explicitly commit the transaction
except SQLAlchemyError as e:
    print(f"An error occurred: {e}")

