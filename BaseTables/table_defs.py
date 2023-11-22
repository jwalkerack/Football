Games = """
    CREATE TABLE IF NOT EXISTS Games (
        id INT AUTO_INCREMENT PRIMARY KEY,
        homeTeam VARCHAR(255) NOT NULL,
        awayTeam VARCHAR(255) NOT NULL,
        gameWeek INT NOT NULL
    );
"""

Teams = """
    CREATE TABLE IF NOT EXISTS Teams (
        id INT AUTO_INCREMENT PRIMARY KEY,
        teamName VARCHAR(255) NOT NULL
    );
"""

GameWeeks = """
    CREATE TABLE IF NOT EXISTS GameWeeks (
        id INT AUTO_INCREMENT PRIMARY KEY,
        gameWeekName VARCHAR(255) NOT NULL,
        HasBeenPlayed BOOLEAN NOT NULL DEFAULT 0
    );
"""

GameStats = """
    CREATE TABLE IF NOT EXISTS GameStats (
           id INT AUTO_INCREMENT PRIMARY KEY,
    gameId INT,
    HomePossession FLOAT,
    HomeYellow INT,
    HomeRed INT,
    HomeShots INT,
    HomeShotsOnTarget INT,
    HomeTouches INT,
    HomeTouchesInFinalThird INT,
    AwayPossession FLOAT,
    AwayYellow INT,
    AwayRed INT,
    AwayShots INT,
    AwayShotsOnTarget INT,
    AwayTouches INT,
    AwayTouchesInFinalThird INT,
    HomeScore INT ,
    AwayScore INT ,
    matchOutcome VARCHAR(255) NOT NULL,
    FOREIGN KEY (gameId) REFERENCES Games(id)
    );
"""

RunningTable = """
    CREATE TABLE IF NOT EXISTS RunningTable (
           id INT AUTO_INCREMENT PRIMARY KEY,
    Pos INT,

    TeamId INT,
    TeamName VARCHAR(255),
    Played INT ,
    Won INT,
    Lost INT,
    Drawn INT,
    GoalsFor INT,
    GoalsAgaisnt INT,
    GoalDifference INT,
    Points  INT,
    createdDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ModifiedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP);
"""

DWG = """
    CREATE TABLE IF NOT EXISTS datawarehouse (
           id INT AUTO_INCREMENT PRIMARY KEY,
    TeamId INT,
    TeamName VARCHAR(255),
    Position INT ,
    Points INT,
    modDate TIMESTAMP);
"""


Tables = [Games,Teams,GameWeeks,GameStats,RunningTable,DWG]