teams = [
    "Aberdeen",
    "Celtic",
    "Dundee",
    "Dundee United",
    "Dunfermline Athletic",
    "Falkirk",
    "Gretna",
    "Hamilton Academical",
    "Heart of Midlothian",
    "Hibernian",
    "Inverness CT",
    "Kilmarnock",
    "Livingston",
    "Motherwell",
    "Partick Thistle",
    "Rangers",
    "Ross County",
    "St Johnstone",
    "St Mirren",
    "Buckie United"
]

import pandas as pd

df = pd.DataFrame(teams, columns=['teamName'])

from sqlalchemy import create_engine

db_name ='Football'

# Make sure the username, password, host, and port are consistent with your Docker configuration
engine = create_engine(f'mysql+mysqlconnector://root:example@localhost:3307/{db_name}')
try:
    df.to_sql(name='Teams', con=engine, if_exists='append', index=False)
    print("Data successfully written to Teams Table.")
except Exception as e:
    print(f"An error occurred: {e}")