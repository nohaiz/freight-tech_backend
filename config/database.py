# IMPORTS TO INTERACT WITH THE OS AND TO CONNECT POSTGRESQL DATABASE

import os
import psycopg2

# DATABASE CONNECTION 

def get_db_connection():
    connection = psycopg2.connect(
        host=os.environ['POSTGRES_HOST'],
        database=os.environ['POSTGRES_DBNAME'],
        user=os.environ['POSTGRES_USER'],
    )
    return connection
