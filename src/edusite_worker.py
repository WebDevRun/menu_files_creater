from pathlib import Path
from typing import List, NamedTuple
from aiohttp import ClientSession


class EdusitePath(NamedTuple):
    login: str
    upload_file: str
    publish_site: str


class EdusiteWorker:
    site_url = "https://cp.edusite.ru"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }
    session_key = "PHPSESSID"
    edusite_path = EdusitePath(
        "/registered/index.php",
        "/registered/file_upload.php",
        "/registered/eduinfofinish.php",
    )
    error_message = "Не удалось войти на сайт"

    def __init__(self, login: str, password: str) -> None:
        self.login = login
        self.password = password

    async def __login(self, session: ClientSession):
        post_data = {"loginusername": self.login, "loginpasswd": self.password}

        async with session.post(self.edusite_path.login, data=post_data) as response:
            return response

    async def __upload_file(self, session: ClientSession, file_path: Path):
        payload = {
            "formId": "10202",
            "handler": "dailyMenu",
            "filename": file_path.stem,
            "destdir": "food",
            "rename": "filename",
            "action": "addreplacement",
            "description": "",
            "dailyMenu": open(file_path, "rb"),
        }

        async with session.post(
            self.edusite_path.upload_file, data=payload
        ) as response:
            return response

    async def push_files(self, saved_file_paths: List[Path]):
        async with ClientSession(self.site_url, headers=self.headers) as session:
            response = await self.__login(session)

            if self.session_key not in response.cookies:
                raise ValueError(self.error_message)

            session.headers.add("X-Requested-With", "XMLHttpRequest")

            for file_path in saved_file_paths:
                session.headers.add("X-File-Name", file_path.stem)
                response = await self.__upload_file(session, file_path)
                session.headers.pop("X-File-Name")
