import streamlit as st
import subprocess
import pandas as pd
from sqlalchemy import create_engine

def display_points_over_time():
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    # Database connection
    engine = create_engine('mysql+mysqlconnector://root:example@localhost:3307/Football')
    query = "SELECT TeamName, Points, modDate FROM datawarehouse"
    df = pd.read_sql(query, engine)

    # Let the user select teams
    teams = df['TeamName'].unique()
    selected_teams = st.multiselect("Select Teams", teams)

    if selected_teams:
        # Filter dataframe for selected teams
        filtered_df = df[df['TeamName'].isin(selected_teams)]

        # Creating a mapping for game weeks
        unique_dates = sorted(filtered_df['modDate'].unique())
        date_to_gw = {date: f'GW-{i + 1}' for i, date in enumerate(unique_dates)}

        # Replacing dates with numerical game week IDs in the DataFrame
        filtered_df['GameWeek'] = filtered_df['modDate'].map(date_to_gw)

        # Determine the maximum points value
        max_points = filtered_df['Points'].max()

        # Plotting
        plt.figure(figsize=(10, 6))
        for team in selected_teams:
            team_df = filtered_df[filtered_df['TeamName'] == team]
            plt.plot(range(len(unique_dates)), team_df['Points'], label=team, marker='o')

        # Dynamic adjustment of the y-axis
        plt.ylim(0, max_points + 5)  # Adding a buffer for better visibility
        plt.yticks(range(0, max_points + 1, max(max_points // 10, 1)))  # Adjusting y-ticks

        # Adjusting the x-axis for Game Weeks
        plt.xticks(range(len(unique_dates)), date_to_gw.values(), rotation=45)

        # Axis labels and title
        plt.xlabel('Game Week')
        plt.ylabel('Points')
        plt.title('Team Points Over Time')

        # Legend and displaying the plot
        plt.legend()
        st.pyplot(plt)


def display_team_performance():
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    # Database connection
    engine = create_engine('mysql+mysqlconnector://root:example@localhost:3307/Football')
    query = "SELECT TeamName, Position, modDate FROM datawarehouse"
    df = pd.read_sql(query, engine)

    # Let the user select teams
    teams = df['TeamName'].unique()
    selected_teams = st.multiselect("Select Teams", teams)

    if selected_teams:
        # Filter dataframe for selected teams
        filtered_df = df[df['TeamName'].isin(selected_teams)]

        # Creating a mapping for game weeks
        unique_dates = sorted(filtered_df['modDate'].unique())
        date_to_gw = {date: f'GW-{i + 1}' for i, date in enumerate(unique_dates)}

        # Replacing dates with numerical game week IDs in the DataFrame
        filtered_df['GameWeek'] = filtered_df['modDate'].map(date_to_gw)

        # Plotting
        plt.figure(figsize=(10, 6))
        for team in selected_teams:
            team_df = filtered_df[filtered_df['TeamName'] == team]
            plt.plot(range(len(unique_dates)), team_df['Position'], label=team, marker='o')

        # Adjusting the y-axis
        plt.ylim(0, 21)
        plt.yticks(range(1, 21))

        # Adjusting the x-axis for Game Weeks
        plt.xticks(range(len(unique_dates)), date_to_gw.values(), rotation=45)

        # Axis labels and title
        plt.xlabel('Game Week')
        plt.ylabel('Position')
        plt.title('Team Positions Over Time')

        # Legend and displaying the plot
        plt.legend()
        st.pyplot(plt)


# Function to start the process of setting up the league
def start_process():
    try:
        subprocess.run(["python", "./BaseTables/1_table_build.py"], check=True)
        subprocess.run(["python", "./BaseDataGeneration/1populateTeams.py"], check=True)
        subprocess.run(["python", "./BaseDataGeneration/2populateGames.py"], check=True)
        subprocess.run(["python", "./BaseDataGeneration/3populateGamesWeeks.py"], check=True)
        subprocess.run(["python", "./BaseDataGeneration/4populateTable.py"], check=True)
        #subprocess.Popen(["python", "./Poll/read_save_mesg.py"])
        subprocess.Popen(["python", "./Poll/send_mesg_only.py"])
        st.session_state["league_set_up"] = True
        st.session_state["display"] = True
        return True
    except subprocess.CalledProcessError as e:
        st.write(f"An error occurred: {e}")
        return False

# Function to display the RunningTable
def display_table():
    engine = create_engine('mysql+mysqlconnector://root:example@localhost:3307/Football')
    query = "SELECT * FROM RunningTable"
    df = pd.read_sql(query, engine)
    df = df.drop(['id', 'TeamId','createdDate','ModifiedDate'], axis=1)
    df = df.rename(columns={'Pos': '#', 'GoalsFor': '+', 'GoalsAgaisnt': '-', 'GoalDifference': 'GD'})
    df.set_index('#', inplace=True)
    st.dataframe(df)

def display_table_running():
    engine = create_engine('mysql+mysqlconnector://root:example@localhost:3307/Football')
    query = "SELECT * FROM datawarehouse"
    df = pd.read_sql(query, engine)
    st.dataframe(df)

# Function to restart the league process

def stop_poll_process():
    if "poll_process" in st.session_state and st.session_state["poll_process"]:
        st.session_state["poll_process"].terminate()  # Terminate the process
        st.session_state["poll_process"].wait()  # Wait for the process to terminate
        st.session_state["poll_process"] = None
        st.write("Poll process terminated successfully.")
def restart_process():
    stop_poll_process()
    try:
        subprocess.run(["python", "./Restart/DropFootball.py"], check=True)
        st.write("Restart process completed successfully!")
        st.session_state.league_set_up = False
        if "display" in st.session_state:
            del st.session_state["display"]
        return True
    except subprocess.CalledProcessError as e:
        st.write(f"An error occurred during restart: {e}")
        return False

# Function to play games and update the league
def play_games_and_update():
    import time
    try:
        subprocess.run(["python", "./PlayGames/1_playgameWeek.py"], check=True)
        subprocess.run(["python", "./PlayGames/2_make_League.py"], check=True)
        st.write("Games played and league updated successfully!")
        time.sleep(2)
        st.session_state["display"] = True
    except subprocess.CalledProcessError as e:
        st.write(f"An error occurred: {e}")

# Initialize session state variables
if "league_set_up" not in st.session_state:
    st.session_state.league_set_up = False
if "display" not in st.session_state:
    st.session_state.display = False
import time



# Streamlit app layout
st.title("Football League")
st.text("Process Buttons")
# Button logic
if not st.session_state.league_set_up:
    # Show only 'Set Up League' button if the league is not set up
    if st.button("Set Up League"):
        if start_process():
            st.write("League setup process completed successfully!")
            st.session_state.league_set_up = True  # Ensure state is updated
            st.experimental_rerun()  # Force UI update
else:

    # Show 'Play Games' and 'Restart League' buttons if the league is set up
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Play Games"):
            play_games_and_update()
    with col2:
        if st.button("Delete League"):
            if restart_process():
                st.experimental_rerun()

# Display tabs only if the league is set up
if st.session_state.league_set_up:
    tab = st.radio("Choose a view", ('Show League', 'Show Position Over Time', 'Show Points Over Time'))

    if tab == 'Show League':
        display_table()  # Your function to display the league table
    elif tab == 'Show Position Over Time':
        display_team_performance()  # Your existing function
    elif tab == 'Show Points Over Time':
        display_points_over_time()  # You need to define this function



