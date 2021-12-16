import psycopg2
import config


def show():
    connection = psycopg2.connect(
        host=config.host,
        user=config.user,
        password=config.password,
        database=config.db_name
    )
    connection.autocommit = True

    print("teacher's table:")
    with connection.cursor() as cursor:
        result = cursor.execute(f"""SELECT * FROM teacher""")
        result = cursor.fetchall()
    for teacher in result:
        print(teacher)

    print("subject's table:")
    with connection.cursor() as cursor:
        result = cursor.execute(f"""SELECT name FROM subject""")
        result = cursor.fetchall()
    for name in result:
        print(name)

    print("timetable's table:")
    with connection.cursor() as cursor:
        result = cursor.execute(f"""SELECT * FROM timetable""")
        result = cursor.fetchall()
    for element in result:
        print(element)

show()