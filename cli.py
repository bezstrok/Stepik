import asyncio
import re
import typing
from pprint import pprint
from urllib.parse import urljoin

import fire
import httpx

API_HOST = "https://stepik.org"

CLIENT_ID = "IiVteX4xyAKDD2cQqqjAgtbDuwZes5qNQYCQVBf3"
CLIENT_SECRET = "5YnByCxjqCXRnkxhJuAj64CsPcWaEVaGcG8Sw6JeOkwVJymDIZ3yAY5A2NbKdFmUG32WMtvB7qcbRF9n0mN6d7z5G2DjzpjMrhC1z65m48hbaGFlubXpBDNoHij3Bjpc"


class Endpoints:
    token = "/oauth2/token/"
    courses = "/api/courses/"


class Sanitizer:
    def __init__(self, repl: str = " ") -> None:
        self._repl = repl
        self._pattern = re.compile(r'[<>:"/\\|?*]')

    def __call__(self, string: str) -> str:
        return self._pattern.sub(self._repl, string)


class Fetcher:
    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    async def post(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        response = await self._client.post(*args, **kwargs)
        response.raise_for_status()
        return response.json()

    async def get(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        response = await self._client.get(*args, **kwargs)
        response.raise_for_status()
        return response.json()

    async def get_paginated(self, *args: typing.Any, **kwargs: typing.Any) -> list[typing.Any]:
        objects: list[typing.Any] = []
        page = 1
        while True:
            params = {**kwargs.pop("params", {}), "page": page}
            data = await self.get(*args, params=params, **kwargs)
            objects.append(data)
            if not data["meta"]["has_next"]:
                break
            page += 1
        return objects


class Parser:
    @staticmethod
    def extract_token(data: typing.Any) -> str:
        if not isinstance(data, typing.Mapping):
            raise TypeError(f"Expected mapping, got {type(data)}")
        if not "access_token" in data:
            raise KeyError("access_token")
        return data["access_token"]

    @staticmethod
    def extract_object(data: typing.Any) -> dict[str, typing.Any]:
        return Parser.extract_objects(data)[0]

    @staticmethod
    def extract_objects(data: typing.Any) -> list[dict[str, typing.Any]]:
        if not isinstance(data, typing.Mapping):
            raise TypeError(f"Expected mapping, got {type(data)}")
        key = next(iter(d for d in data if d != 'meta'))
        return list(map(dict, data[key]))

    @staticmethod
    def extract_objects_from_list(data_list: typing.Iterable[typing.Any]) -> list[dict[str, typing.Any]]:
        data_list = list(data_list)
        if not data_list:
            return []
        if not all(isinstance(data, typing.Mapping) for data in data_list):
            raise TypeError(f"Expected list of mappings, got {type(data_list[0])}")
        key = next(iter(d for d in data_list[0] if d != 'meta'))
        objects: list[dict[str, typing.Any]] = []
        for data in data_list:
            objects.extend(data[key])
        return objects





class CLI:
    def __init__(
        self,
        *,
        fetcher: Fetcher,
        parser: Parser,
        sanitizer: Sanitizer,
    ) -> None:
        self._fetcher = fetcher
        self._parser = parser
        self._sanitizer = sanitizer

    async def sync_course(self, course_id: int) -> str:
        course_info = await self._get_course_info(course_id)
        pprint(course_info)

    async def _get_course_info(self, course_id: int) -> dict[str, typing.Any]:
        return self._parser.extract_object(
            await self._fetcher.get(
                urljoin(Endpoints.courses, f"{course_id}")
            )
        )


if __name__ == "__main__":
    event_loop = asyncio.get_event_loop()

    client_instance = httpx.AsyncClient(base_url=API_HOST)
    fetcher_instance = Fetcher(client_instance)
    parser_instance = Parser()
    sanitizer_instance = Sanitizer()

    access_token = event_loop.run_until_complete(get_access_token(fetcher_instance, parser_instance))
    update_access_token(client_instance, access_token)

    fire.Fire(
        CLI(
            fetcher=fetcher_instance,
            parser=parser_instance,
            sanitizer=sanitizer_instance,
        )
    )
