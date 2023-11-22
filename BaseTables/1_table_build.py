from table_defs import Tables

def create_tables(database,config ,tables):

    import re
    import mysql.connector
    cnx = mysql.connector.connect(**config)
    if cnx.is_connected():
        print("Connection is Open !!")
        cursor = cnx.cursor()
        dbQuery =  f"CREATE DATABASE IF NOT EXISTS {database};"
        cursor.execute(dbQuery)
        cursor.execute(f"USE {database};")
        for table in tables:
            try:
                cursor.execute(table)
                cnx.commit()
                pattern = r"CREATE TABLE IF NOT EXISTS\s+(\w+)\s*\("
                match = re.search(pattern, table)
                if match:
                    table_name = match.group(1)

                else:
                    table_name = "Table name not found"
                print (f"The {table_name} has been created")
            except OSError as e:
                print (f"The {table} creation contained errors - {e}")

        cursor.close()
        cnx.close()

config = {
    'user': 'root',
    'password': 'example',  # Use your root password here
    'host': 'localhost',
    'port': 3307,
}

database = 'Football'

create_tables(database,config ,Tables)