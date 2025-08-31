import asyncio
import os

import dotenv
import fire
import httpx

from tools.cli import CLI
from tools.fetcher import AsyncFetcherProtocol, AsyncFetcher
from tools.parser import Parser
from tools.sanitizer import Sanitizer
from tools.urls import Endpoints, API_HOST


def get_client_credentials_from_env() -> tuple[str, str]:
    return os.getenv("CLIENT_ID"), os.getenv("CLIENT_SECRET")


async def get_access_token(
    client_id: str,
    client_secret: str,
    *,
    fetcher: AsyncFetcherProtocol,
) -> str:
    data = await fetcher.post(
        Endpoints.token,
        data={"grant_type": "client_credentials"},
        auth=(client_id, client_secret),
    )
    return data["access_token"]


def update_access_token(client: httpx.AsyncClient, token: str) -> None:
    client.headers.update({"Authorization": f"Bearer {token}"})


if __name__ == "__main__":
    dotenv.load_dotenv()

    event_loop = asyncio.get_event_loop()

    client_instance = httpx.AsyncClient(base_url=API_HOST)
    fetcher_instance = AsyncFetcher(client_instance)
    parser_instance = Parser()
    sanitizer_instance = Sanitizer()

    access_token = event_loop.run_until_complete(
        get_access_token(
            *get_client_credentials_from_env(),
            fetcher=fetcher_instance,
        )
    )
    update_access_token(client_instance, access_token)

    fire.Fire(
        CLI(
            fetcher=fetcher_instance,
            parser=parser_instance,
            sanitizer=sanitizer_instance,
        )
    )
