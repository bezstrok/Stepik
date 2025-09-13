import asyncio
import os

import dotenv
import fire
import httpx
import jinja2

from tools.cleaner import FilenameCleaner, HTMLCleaner
from tools.cli import CLI
from tools.fetcher import AsyncFetcher, AsyncFetcherProtocol
from tools.parser import Parser
from tools.renderers.course import CourseRendered
from tools.renderers.section import SectionRendered
from tools.urls import API_HOST, Endpoints
from tools.workspace import Workspace


def get_client_credentials_from_env() -> tuple[str, str]:
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")

    if client_id is None:
        raise ValueError("CLIENT_ID must be set in the environment")
    if client_secret is None:
        raise ValueError("CLIENT_SECRET must be set in the environment")

    return client_id, client_secret


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


def inject_access_token_to_http_client(client: httpx.AsyncClient, token: str) -> None:
    client.headers.update({"Authorization": f"Bearer {token}"})


if __name__ == "__main__":
    dotenv.load_dotenv()

    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)

    http_client = httpx.AsyncClient(
        base_url=API_HOST,
        follow_redirects=True,
    )

    fetcher = AsyncFetcher(http_client)
    parser = Parser()

    filename_sanitizer = FilenameCleaner()
    html_sanitizer = HTMLCleaner()

    workspace = Workspace(
        "courses",
        filename_sanitizer,
    )

    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader("tools/templates"))
    course_generator = CourseRendered(
        jinja_env.get_template("course.jinja"),
        html_sanitizer,
    )
    section_generator = SectionRendered(
        jinja_env.get_template("section.jinja"),
        html_sanitizer,
    )

    access_token = event_loop.run_until_complete(
        get_access_token(
            *get_client_credentials_from_env(),
            fetcher=fetcher,
        )
    )
    inject_access_token_to_http_client(http_client, access_token)

    fire.Fire(
        CLI(
            workspace=workspace,
            fetcher=fetcher,
            parser=parser,
            course_generator=course_generator,
            section_generator=section_generator,
        )
    )
