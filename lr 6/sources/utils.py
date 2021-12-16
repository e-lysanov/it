
import calendar
import datetime


def stamp_day_of_week(day_of_week):
    return day_of_week.replace("_чет", "").replace("_нечет", "")


def concatenate(day, even):
    if even:
        return day+"_нечет"
    else:
        return day+"_чет"


FORMATTED_DAY = '{0} [{1}] {2} {3}'
# функция, определяющая номер текущей недели


def is_week_even(time_now):
    stringify = time_now.strftime("%d %m %Y").split()
    day, month, year = int(stringify[0]), int(stringify[1]), int(stringify[2])
    calendar_ = calendar.TextCalendar(calendar.MONDAY)
    lines = calendar_.formatmonth(year, month).split('\n')
    days_by_week = [week.lstrip().split() for week in lines[2:]]
    str_day = str(day)
    for index, week in enumerate(days_by_week):
        if str_day in week:
            return index % 2 != 0

