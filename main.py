from pathlib import Path
from src.ini_reader import IniReader
from src.date_generator import DateGenerator
from src.openpyxl_worker import OpenpyxlWorker


def main():
    config_path = Path("dates.ini").absolute()
    config_dates = IniReader(config_path).get_dates()
    generated_dir_name = f"{config_dates.start_date}-{config_dates.end_date}"
    dates = DateGenerator.generate_from_string(
        config_dates.first_education_date,
        config_dates.start_date,
        config_dates.end_date,
    )
    dateGenerator = DateGenerator(
        dates.first_education_date,
        dates.start_date,
        dates.end_date,
        config_dates.education_day_count,
    )
    date_info = dateGenerator.generate_date_range()
    template_files = [
        Path("templates", f"{number}.xlsx").absolute()
        for number in date_info.date_indexes
    ]
    save_dir = Path(generated_dir_name)
    save_dir.mkdir(exist_ok=True)
    OpenpyxlWorker(date_info.dates, template_files, save_dir).generate_files()


if __name__ == "__main__":
    main()
