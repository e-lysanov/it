import psycopg2
import config
conn = psycopg2.connect(database=config.db_connect['database'],
                        user=config.db_connect['user'],
                        password=config.db_connect['password'],
                        host=config.db_connect['host'],
                        port=config.db_connect['port'])
cursor = conn.cursor() 
with open('schema.sql') as f:
    cursor.execute(f.read())
conn.commit()
conn.close()