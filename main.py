from pathlib import Path
from asyncio import run as aio_run

from src.load_env import LoadEnv
from src.edusite_worker import EdusiteWorker
from src.ini_reader import IniReader
from src.date_generator import DateGenerator
from src.openpyxl_worker import OpenpyxlWorker

options_ini = "options.ini"
templates_folder = "templates"
no_auth_message = "не указан логин и/или пароль"


async def main():
    auth_config = LoadEnv().load()

    if auth_config is None:
        raise ValueError(no_auth_message)

    config_path = Path(options_ini).resolve()
    config_dates = IniReader(config_path).get_dates()
    generated_dir_name = f"{config_dates.start_date}-{config_dates.end_date}"
    dates = DateGenerator.generate_from_string(
        config_dates.first_education_date,
        config_dates.start_date,
        config_dates.end_date,
    )
    date_info = DateGenerator(
        dates.first_education_date,
        dates.start_date,
        dates.end_date,
        config_dates.education_day_count,
    ).generate_date_range()
    template_files = [
        Path(templates_folder).joinpath(f"{index}.xlsx").resolve()
        for index in date_info.date_indexes
    ]
    save_dir = Path(generated_dir_name)

    openpyxl_worker = OpenpyxlWorker(date_info.dates, template_files, save_dir)
    saved_file_paths = openpyxl_worker.generate_files()

    edusite_worker = EdusiteWorker(auth_config.login, auth_config.password)
    await edusite_worker.push_files(saved_file_paths)


if __name__ == "__main__":
    aio_run(main())
