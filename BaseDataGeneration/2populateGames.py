import itertools
import random


def round_robin_teams(teams):
    """ Generate a round-robin schedule for the given number of teams. """
    if len(teams) % 2:
        teams.append(None)  # if number of team is odd, add a dummy team for bye weeks

    rotation = list(teams)  # copy the list
    schedule = []
    for i in range(len(teams) - 1):
        matches = []
        for j in range(len(teams) // 2):
            if rotation[j] is not None and rotation[-j - 1] is not None:
                matches.append((rotation[j], rotation[-j - 1]))
        schedule.append(matches)
        rotation.insert(1, rotation.pop())  # rotate for next round
    return schedule


def Generate_Dataframe(round_robin_schedule):
    import pandas as pd
    count = 1
    Data = []
    for item in round_robin_schedule:
        for match in item:
            row = list(match) + [count]
            Data.append(row)
        count += 1
    df = pd.DataFrame(Data, columns=['HomeTeam', 'AwayTeam', 'GameWeek'])
    return df


def GenerateRandomDict(teams):
    import copy
    import random
    deep_copied_list = copy.deepcopy(teams)
    random.shuffle(deep_copied_list)
    OrderDict = {}
    for index, key in enumerate(deep_copied_list):
        OrderDict[teams[index]] = key + 100
    return OrderDict


def processDataFrame(dataframe, dictionary):
    import pandas as pd
    import copy
    df_copy = dataframe.copy()
    df_copy['GameWeek2'] = 0
    df_copy['GameWeek2'] = df_copy['GameWeek'].map(dictionary)
    df_copy.drop('GameWeek', axis=1, inplace=True)
    df_copy.rename(columns={'GameWeek2': 'GameWeek'}, inplace=True)
    y = pd.concat([dataframe, df_copy], ignore_index=True)
    sorted_result_df = y.sort_values(by='GameWeek')
    sorted_result_df['GameWeekY'] = pd.factorize(sorted_result_df['GameWeek'])[0] + 1
    sorted_result_df.drop('GameWeek', axis=1, inplace=True)
    sorted_result_df.rename(columns={'GameWeekY': 'GameWeek'}, inplace=True)
    sorted_result_df.rename(columns={'HomeTeam': 'homeTeam',
                                     'AwayTeam': 'awayTeam',
                                     'GameWeek': 'gameWeek'}, inplace=True)
    return sorted_result_df


teams = list(range(1, 21))
round_robin_schedule = round_robin_teams(teams)
DataFrame = Generate_Dataframe(round_robin_schedule)
OrderDict = GenerateRandomDict(teams)
DataForDb = processDataFrame(DataFrame , OrderDict)

from sqlalchemy import create_engine

# Replace 'mysqlconnector' with 'pymysql' if you are using PyMySQL
# Make sure the username, password, host, and port are consistent with your Docker configuration
engine = create_engine('mysql+mysqlconnector://root:example@localhost:3307/Football')

try:
    DataForDb.to_sql(name='Games', con=engine, if_exists='append', index=False)
    print("Data successfully written to Games Table.")
except Exception as e:
    print(f"An error occurred: {e}")