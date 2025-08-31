import typing
from pprint import pprint
from urllib.parse import urljoin

from tools.urls import Endpoints
from tools.fetcher import AsyncFetcherProtocol
from tools.parser import ParserProtocol
from tools.sanitizer import SanitizerProtocol


class CLI:
    def __init__(
        self,
        *,
        fetcher: AsyncFetcherProtocol,
        parser: ParserProtocol,
        sanitizer: SanitizerProtocol,
    ) -> None:
        self._fetcher = fetcher
        self._parser = parser
        self._sanitizer = sanitizer

    async def sync_course(self, course_id: int) -> str:
        course_info = await self._get_course_info(course_id)
        pprint(course_info)
        return "ok"

    async def _get_course_info(self, course_id: int) -> dict[str, typing.Any]:
        return self._parser.extract_object(
            await self._fetcher.get(
                urljoin(Endpoints.courses, f"{course_id}")
            )
        )
