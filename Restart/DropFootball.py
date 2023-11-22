

def CreateConnection(config):
    import mysql.connector
    connection = mysql.connector.connect(**config)
    return connection


config = {
    'user': 'root',
    'password': 'example',  # Use your root password here
    'host': 'localhost',
    'port': 3307,
}

connection = CreateConnection(config)
if connection.is_connected():
    print("connection is closed.")
    cursor = connection.cursor()
    db_name ='Football'
    try:
        cursor.execute(f"DROP DATABASE IF EXISTS {db_name};")
        print (f"DATABASE {db_name} has been dropped")
    except Error as e:
        print (f"There was an Error : {e}")
    cursor.close()
    connection.close()
    print("connection is closed.")



from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import KafkaError

def delete_kafka_topic(topic_name, bootstrap_servers):
    """
    Delete a Kafka topic.

    :param topic_name: Name of the Kafka topic to be deleted.
    :param bootstrap_servers: List of bootstrap servers for the Kafka cluster.
    """
    try:
        admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
        admin_client.delete_topics([topic_name])
        print(f"Topic '{topic_name}' deleted successfully.")
    except KafkaError as e:
        print(f"An error occurred: {e}")
    finally:
        admin_client.close()

# Usage
bootstrap_servers = ['localhost:9092']  # Replace with your Kafka server address
topic_name = 'league_position_updates'  # Replace with the name of your topic

delete_kafka_topic(topic_name, bootstrap_servers)

# Usage


