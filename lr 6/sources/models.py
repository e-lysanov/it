from dataclasses import dataclass
import utils


@dataclass
class Subject:
    name: str
    start_time: str
    room: str
    teacher: str

    @staticmethod
    def get_teacher_by_subject_name(name, connection):
        result = None
        with connection.cursor() as cursor:
            result = cursor.execute(f"""SELECT full_name FROM 
                                        teacher 
                                        WHERE 
                                        subject='{name}'""")
            result = cursor.fetchall()
        if len(result) == 0:
            return None
        else:
            return result[0][0]


@dataclass
class DaySchedule:
    subjects: list
    name: str

    def represent(self, connection):
        result = f"{self.name}\n"
        for index, subject in enumerate(self.subjects):
            result += f"{index + 1}) " + utils.FORMATTED_DAY.format(subject.name,
                                                                    subject.room,
                                                                    subject.start_time,
                                                                    Subject.get_teacher_by_subject_name(subject.name,
                                                                                                        connection)) \
                      + '\n'

        return result

    @staticmethod
    def get_day_schedule_by_day_name(day_name, even, connection):
        day_name_in_db = utils.concatenate(day_name, even)
        result = None
        with connection.cursor() as cursor:
            result = cursor.execute(f"""SELECT * FROM 
                                        timetable 
                                        WHERE 
                                        day='{day_name_in_db}'""")
            result = cursor.fetchall()
        subjects = list([Subject(name=record[2],
                                 start_time=record[4],
                                 room=record[3],
                                 teacher=Subject.get_teacher_by_subject_name(record[2], connection))
                         for record in result])
        return DaySchedule(name=day_name, subjects=subjects)
