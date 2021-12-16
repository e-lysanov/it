import psycopg2
import config


def configure():
    # --------CONNECTING TO DB-----------
    connection = psycopg2.connect(
        host=config.host,
        user=config.user,
        password=config.password,
        database=config.db_name
    )
    connection.autocommit = True

    # --------DROP TABLES------------

    with connection.cursor() as cursor:
        cursor.execute("""DROP TABLE IF EXISTS subject CASCADE;
                          DROP TABLE IF EXISTS teacher CASCADE;
                          DROP TABLE IF EXISTS timetable CASCADE;""")


    # --------CREATE TABLES-----------

    with connection.cursor() as cursor:
         cursor.execute("""CREATE TABLE subject(name varchar(150) primary key);""")


    with connection.cursor() as cursor:
         cursor.execute(
             """CREATE TABLE timetable(
                  id serial primary key,
                  day varchar(30),
                  subject varchar(150) references subject(name),
                  room_number varchar(10),
                  start_time varchar(30));"""
         )

    with connection.cursor() as cursor:
            cursor.execute(
                """CREATE TABLE teacher(
                    id serial PRIMARY KEY,
                    full_name varchar(150) NOT NULL,
                    subject varchar(150) references subject(name));"""
            )


    # -------INSERTING VALUES------
    with connection.cursor() as cursor:
        cursor.execute(
            """INSERT INTO subject(name) VALUES
            ('Высш. мат. пр.з. 7-17 нед.'), ('Ин.яз пр.з.'), ('ТВиМС пр.з.'), ('Элективные дисц. по физической культуре'), 
            ('лек. Правоведение'), ('лек. Введение в ИТ'), ('лек. Электроника'),
            ('лек. Экология'), ('пр. Экология'),('лек. ТВиМС'), ('лек. История развития средств связи'), 
            ('История развития средств связи пр.з.'), ('лек. Выч. техника'), ('лек. Высш. мат.'), ('Правоведение пр.з.'),
            ('Введение в ИТ лаб.'), ('Введение в ИТ пр.з.'), ('Основы компьютерного анализа ЭЦ лаб.'), ('Электроника лаб.'),
            ('Выч. техника лаб.');"""
        )

    with connection.cursor() as cursor:
        cursor.execute(
            """INSERT INTO teacher (full_name, subject) VALUES
                ( 'Александров Ю.Л.', (SELECT name from subject WHERE name='Высш. мат. пр.з. 7-17 нед.')),
                ( 'Александров Ю.Л.', (SELECT name from subject WHERE name ='лек. Высш. мат.')),
                ( 'Антипов А.А.', (SELECT name from subject WHERE name ='Правоведение пр.з.')),
                ( 'Антипов А.А.', (SELECT name from subject WHERE name='лек. Правоведение')),
                ( 'Сретенская Н.В.', (SELECT name from subject WHERE name='лек. Электроника')),
                ( 'Ерофеева В.В.', (SELECT name from subject WHERE name='лек. Экология')),
                ( 'Ерофеева В.В.', (SELECT name from subject WHERE name ='пр. Экология')),
                ( 'Панков К.Н.', (SELECT name from subject WHERE name='ТВиМС пр.з.')),
                ( 'Панков К.Н.', (SELECT name from subject WHERE name ='лек. ТВиМС')),
                ( 'Калабекьянц Н.Э.', (SELECT name from subject WHERE name='лек. История развития средств связи')),
                ( 'Калабекьянц Н.Э.', (SELECT name from subject WHERE name ='История развития средств связи пр.з.')),
                ( 'Селезнев В.С.', (SELECT name from subject WHERE name='Выч. техника лаб.')),
                ( 'Селезнев В.С.', (SELECT name from subject WHERE name ='лек. Выч. техника')),
                ( 'Степанова А.Г.', (SELECT name from subject WHERE name='Основы компьютерного анализа ЭЦ лаб.'));"""
        )

    with connection.cursor() as cursor:
        cursor.execute(
            """INSERT INTO timetable(day, room_number, subject, start_time) values 
            ('Понедельник_чет', '224', (SELECT name from subject WHERE name='Высш. мат. пр.з. 7-17 нед.'), '9:30'),  
            ('Понедельник_чет', '347', (SELECT name from subject WHERE name='Высш. мат. пр.з. 7-17 нед.'), '11:20'), 
            ('Понедельник_чет', '450', (SELECT name from subject WHERE name='Ин.яз пр.з.'), '13:10'), 
            ('Понедельник_чет', '224', (SELECT name from subject WHERE name='ТВиМС пр.з.'), '15:25'),
            ('Понедельник_чет', '-', (SELECT name from subject WHERE name='Элективные дисц. по физической культуре'), '17:15'), 
            ('Понедельник_нечет', '224', (SELECT name from subject WHERE name='Высш. мат. пр.з. 7-17 нед.'), '9:30'),  
            ('Понедельник_нечет', '347', (SELECT name from subject WHERE name='Высш. мат. пр.з. 7-17 нед.'), '11:20'), 
            ('Понедельник_нечет', '450', (SELECT name from subject WHERE name='Ин.яз пр.з.'), '13:10'), 
            ('Понедельник_нечет', '224', (SELECT name from subject WHERE name='ТВиМС пр.з.'), '15:25'),
            ('Понедельник_нечет', '-', (SELECT name from subject WHERE name='Элективные дисц. по физической культуре'), '17:15'),
            
            ('Вторник_чет', 'УЛК-2', (SELECT name from subject WHERE name='лек. Правоведение'), '9:30'), 
            ('Вторник_чет', 'УЛК-2', (SELECT name from subject WHERE name='лек. Введение в ИТ'), '11:20'),
            ('Вторник_чет', 'УЛК-2', (SELECT name from subject WHERE name='лек. Электроника'), '13:10'),
            ('Вторник_чет', 'УЛК-2', (SELECT name from subject WHERE name='лек. Экология'), '15:25'),
            ('Вторник_чет', 'УЛК-2', (SELECT name from subject WHERE name='лек. ТВиМС'), '17:15'),
            ('Вторник_нечет', 'Дист.', (SELECT name from subject WHERE name='Выч. техника лаб.'), '15:25'), 
            ('Вторник_нечет', 'Дист.', (SELECT name from subject WHERE name='Выч. техника лаб.'), '17:15'),
            
            ('Среда_чет', 'УЛК-2', (SELECT name from subject WHERE name='лек. Выч. техника'), '13:10'),
            ('Среда_чет', 'УЛК-2', (SELECT name from subject WHERE name='лек. Высш. мат.'), '15:25'),
            ('Среда_нечет', 'УЛК-2', (SELECT name from subject WHERE name='лек. История развития средств связи'), '11:20'),
            ('Среда_нечет', 'УЛК-2', (SELECT name from subject WHERE name='История развития средств связи пр.з.'), '13:10'),
            ('Среда_нечет', 'УЛК-2', (SELECT name from subject WHERE name='лек. Высш. мат.'), '15:25'),
            
            ('Четверг_чет', '339', (SELECT name from subject WHERE name='пр. Экология'), '11:20'),
            ('Четверг_чет', '-', (SELECT name from subject WHERE name='Элективные дисц. по физической культуре'), '13:10'),
            ('Четверг_чет', '224', (SELECT name from subject WHERE name='Введение в ИТ пр.з.'), '15:25'),
            ('Четверг_чет', '224', (SELECT name from subject WHERE name='Введение в ИТ лаб.'), '17:15'),
            ('Четверг_нечет', '404', (SELECT name from subject WHERE name='Правоведение пр.з.'), '11:20'),
            ('Четверг_нечет', '-', (SELECT name from subject WHERE name='Элективные дисц. по физической культуре'), '13:10'),
            ('Четверг_нечет', '224', (SELECT name from subject WHERE name='Введение в ИТ пр.з.'), '15:25'),
            ('Четверг_нечет', '224', (SELECT name from subject WHERE name='Введение в ИТ лаб.'), '17:15'),
            
            ('Пятница_чет', '224', (SELECT name from subject WHERE name='Основы компьютерного анализа ЭЦ лаб.'), '13:10'),
            ('Пятница_чет', '525', (SELECT name from subject WHERE name='Электроника лаб.'), '15:25'),
            ('Пятница_нечет', '224', (SELECT name from subject WHERE name='Основы компьютерного анализа ЭЦ лаб.'), '13:10'),
            ('Пятница_нечет', '525', (SELECT name from subject WHERE name='Электроника лаб.'), '15:25');"""
            )

    if connection:
        connection.close()
