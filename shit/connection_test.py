import psycopg2
from psycopg2 import Error

try:
    connection = psycopg2.connect(user="emirnavruzov",
                                  password="qwe123@#29",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="ormdb")
    cursor = connection.cursor()

    insert_query = '''INSERT INTO ormtable (id ,name) VALUES (3, '1emir test with select');'''
    select_query = '''SELECT * FROM ormtable LIMIT 2 OFFSET 1;'''
    cursor.execute(select_query)
    # cursor.execute(insert_query)
    print(cursor.fetchall())

    connection.commit()
except (Exception, psycopg2.DatabaseError) as error:
    print("Error while creating PostgreSQL table", error)
finally:
    if (connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")


