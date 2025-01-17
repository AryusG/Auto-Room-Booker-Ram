import datetime
from calendar import monthrange
from logging import raiseExceptions


class DateTooLargeError(Exception):
    '''Raised when day number is more than month day total'''
    def __init__(self, message="Input date more than month total of days") -> None:
        super().__init__(message)


class NewDateTwoDaysAhead():
    def __init__(self) -> None:
        self.dt_today = datetime.datetime.today()
        self.today_day = self.dt_today.day
        self.today_month = self.dt_today.month
        self.today_year = self.dt_today.year


    def get_day_month_year(self) -> list:
        '''Returns [day, month, year] from two days ahead'''
        today_day = self.today_day
        today_month = self.today_month
        today_year = self.today_year

        total_month_days = monthrange(today_year, today_month)[1]
        day_difference = total_month_days - today_day #to check if today_date needs to be reset back to 1 or 2 for the new month 

        if day_difference < 0:
            raise DateTooLargeError

        elif today_month != 12 and day_difference == 1:
            print("29")
            today_day = 1
            today_month += 1

        elif today_month != 12 and day_difference == 0:
            print("Not Dec, day difference 0")
            today_day = 2
            today_month += 1

        elif today_month == 12 and day_difference == 1:
            today_day = 1
            today_month = 1
            today_year += 1

        elif today_month == 12 and day_difference == 0:
            today_day = 2
            today_month = 1
            today_year += 1

        elif day_difference > 1:
            today_day += 2

        date_of_next_two = [today_day, today_month, today_year]

        return date_of_next_two


    def get_month_string(self) -> str:
        '''Get string of the Month'''
        next_two_date_list = self.get_day_month_year()
        current_month = next_two_date_list[1]

        months_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                        'August', 'September', 'October', 'November', 'December']
        
        current_month_index = current_month - 1 
        current_month_string = months_list[current_month_index]

        return current_month_string

