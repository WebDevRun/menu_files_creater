from datetime import datetime, timedelta
from typing import NamedTuple


class ConvertedDate(NamedTuple):
    first_education_date: datetime
    start_date: datetime
    end_date: datetime


class DateInfo(NamedTuple):
    dates: list[datetime]
    date_indexes: list[int]


class DateGenerator:
    weekend = (5, 6)

    def __init__(
        self,
        first_education_date: datetime,
        start_date: datetime,
        end_date: datetime,
    ) -> None:
        self.first_education_date = first_education_date
        self.start_date = start_date
        self.end_date = end_date

    @staticmethod
    def generate_from_string(*args: str) -> ConvertedDate:
        dates = [datetime.strptime(date, "%d.%m.%Y") for date in args]
        return ConvertedDate(*dates)

    def __get_day_index_by_date(self, date: datetime, index: int):
        day_number = int(date.strftime("%w"))

        if index >= 2:
            return day_number + 5

        return day_number

    def __get_day_indexes_by_dates(
        self, dates: list[datetime], week_numbers: list[int]
    ):
        return [
            self.__get_day_index_by_date(day, week_numbers[index])
            for index, day in enumerate(dates)
        ]

    def __calculate_week_number(self, date: datetime):
        days = (date - self.first_education_date).days
        week_number = int(days / 7)

        if week_number == 0 or week_number % 2 == 0:
            return 1

        return 2

    def __is_weekday(self, date: datetime):
        return date.weekday() not in self.weekend

    def generate_date_range(self) -> DateInfo:
        days = (self.end_date - self.start_date).days
        dates = [
            date
            for day in range(days + 1)
            if self.__is_weekday(date := self.start_date + timedelta(day))
        ]
        week_numbers = [self.__calculate_week_number(date) for date in dates]
        date_indexes = self.__get_day_indexes_by_dates(dates, week_numbers)

        return DateInfo(
            dates,
            date_indexes,
        )