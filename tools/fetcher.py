import typing

import httpx


class AsyncFetcherProtocol(typing.Protocol):
    async def post(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        pass

    async def get(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        pass

    async def get_paginated(
        self, *args: typing.Any, **kwargs: typing.Any
    ) -> list[typing.Any]:
        pass


class AsyncFetcher:
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

    async def get_paginated(
        self, *args: typing.Any, **kwargs: typing.Any
    ) -> list[typing.Any]:
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
