from datetime import datetime, timezone

class TimeHandler:
    @staticmethod
    def get_next_two_weeks():
        day = datetime.now(timezone.utc)

        days = []

        if day.day + 14 <= day.max.day:
            for i in range(14):
                days.append((TimeHandler.get_weekday_string(day.weekday()), "{0:02d}.{1:02d}.{2}".format(day.day, day.month, day.year)))
                if day.day != day.max.day:
                    day = datetime(day.year, day.month, day.day + 1, day.hour, day.minute, day.second)
        else:
            day_counter = 0
            while day.day <= day.max.day:
                day_counter += 1

                days.append((TimeHandler.get_weekday_string(day.weekday()), "{0:02d}.{1:02d}.{2}".format(day.day, day.month, day.year)))
                try:
                    day = datetime(day.year, day.month, day.day + 1, day.hour, day.minute, day.second)
                except:
                    break

            day = datetime(day.year, day.month + 1, 1, day.hour, day.minute, day.second)
            for i in range(14 - day_counter):
                days.append((TimeHandler.get_weekday_string(day.weekday()), "{0:02d}.{1:02d}.{2}".format(day.day, day.month, day.year)))
                day = datetime(day.year, day.month, day.day + 1, day.hour, day.minute, day.second)
        
        return days
    
    def array_to_date(date):

        day = int(date[0])

        if date[0][0] == '0':
            day = int(date[0][1])

        month = int(date[1])

        if date[1][0] == '0':
            month = int(date[1][1])

        year = int(date[2])

        return datetime(year, month, day, 0, 0, 0)

    @staticmethod
    def get_weekday_string(weekday: int):
        if weekday == 0:
            return "Понедельник"
        elif weekday == 1:
            return "Вторник"
        elif weekday == 2:
            return "Среда"
        elif weekday == 3:
            return "Четверг"
        elif weekday == 4:
            return "Пятница"
        elif weekday == 5:
            return "Суббота"
        elif weekday == 6:
            return "Воскресенье"
        else:
            raise ValueError("weekday value is incorrect")