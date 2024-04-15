import logging
from datetime import datetime
from pathlib import Path
from typing import List
import pylightxl


class OpenpyxlWorker:
    all_files = "*"
    xlsx_format = ".xlsx"
    workbook_name = "1"
    cell_address = "J1"

    def __init__(
        self, dates: List[datetime], path_list: List[Path], save_dir: Path
    ) -> None:
        self.dates = dates
        self.path_list = path_list
        self.save_dir = save_dir

    def __remove_files(self, files_to_remove: List[Path]):
        for file in files_to_remove:
            try:
                file.unlink()
            except OSError as e:
                logging.error(f"Error occurred while removing file: {e}")

    def __create_workbook(self, index: int) -> pylightxl.Database:
        workbook = pylightxl.readxl(self.path_list[index])
        return workbook

    def __update_date(self, workbook: pylightxl.Database, date: datetime) -> None:
        str_date = date.strftime("%d.%m.%Y")
        workbook.ws(self.workbook_name).update_address(self.cell_address, str_date)

    def __write_workbook(self, workbook: pylightxl.Database, date: datetime) -> Path:
        str_date = date.strftime("%Y-%m-%d-sm")
        save_path = Path(self.save_dir, f"{str_date}{self.xlsx_format}")
        self.__update_date(workbook, date)
        pylightxl.writexl(workbook, save_path)
        return save_path

    def __create_save_dir(self) -> None:
        self.save_dir.mkdir(exist_ok=True)

    def __find_files_in_dir(
        self, pattern: str, exception_path: List[Path] = []
    ) -> List[Path]:
        find_files = list(self.save_dir.glob(pattern))

        if len(exception_path) == 0:
            self.__remove_files(find_files)
            return find_files

        files_to_remove = [file for file in find_files if file not in exception_path]
        self.__remove_files(files_to_remove)
        return files_to_remove

    def generate_files(self) -> List[Path]:
        saved_paths = []

        self.__create_save_dir()

        pattern = self.all_files
        self.__find_files_in_dir(pattern)

        for index, date in enumerate(self.dates):
            workbook = self.__create_workbook(index)
            save_path = self.__write_workbook(workbook, date)

            saved_paths.append(save_path)

        pattern = f"{self.all_files}{self.xlsx_format}"
        self.__find_files_in_dir(pattern, saved_paths)
        return saved_paths
