from configparser import ConfigParser
from pathlib import Path
from typing import NamedTuple


class ConfigDates(NamedTuple):
    education_day_count: str
    first_education_date: str
    start_date: str
    end_date: str


class IniReader:
    def __init__(self, path: Path) -> None:
        self.config_path = path

    def __read_file(self):
        config = ConfigParser()
        config.read(self.config_path)
        return config

    def get_dates(self) -> ConfigDates:
        config = self.__read_file()

        education_day_count = config["dates"]["education_day_count"]
        first_education_date = config["dates"]["first_education_date"]
        start_date = config["dates"]["start_date"]
        end_date = config["dates"]["end_date"]

        return ConfigDates(
            education_day_count,
            first_education_date,
            start_date,
            end_date,
        )
