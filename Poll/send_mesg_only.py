
import threading
import json
import time
from datetime import datetime
import mysql.connector
from kafka import KafkaProducer


def write_to_db(db_config,data,table_name):
    import mysql.connector
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    insert_stmt = (
        f"INSERT INTO {table_name} (TeamId, TeamName, Position, Points, modDate) "
        "VALUES (%s, %s, %s, %s, %s)"
    )
    # Insert data
    for record in data:
        cursor.execute(insert_stmt,
                       (record["TeamId"], record["TeamName"], record["Position"], record["Points"], record["modDate"]))
    # Commit and close
    conn.commit()
    cursor.close()
    conn.close()




def poll_database_and_produce(topic_name,db_config):
    last_checked_time = datetime.min
    while True:
        records = query_database(last_checked_time,db_config)
        if records:
            data = [
                {"TeamId": row[0],
                 "TeamName": row[1],
                 "Position": row[2],
                 "Points": row[3],
                 "modDate": row[4].strftime("%Y-%m-%d %H:%M:%S")
                 } for row in records]

            send_to_kafka(data,topic_name)
            write_to_db(db_config, data, 'datawarehouse')
            last_checked_time = records[-1][4]
        time.sleep(2)  # Polling interval in seconds



def query_database(last_checked_time,db_config):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    query = """
    SELECT TeamId, TeamName, Pos, Points, ModifiedDate
    FROM RunningTable
    WHERE ModifiedDate > %s
    """
    cursor.execute(query, (last_checked_time,))
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows

def send_to_kafka(data,topic_name):
    producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    producer.send(topic_name, data)
    producer.flush()
    producer.close()


topic_name = 'football_data'

db_config = {
    "host": "localhost",
    "user": "root",
    'port': 3307,
    "password": "example",
    "database": "Football"}





poller_thread = threading.Thread(target=poll_database_and_produce, args=(topic_name,db_config))
poller_thread.start()
