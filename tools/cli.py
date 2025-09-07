import typing
from urllib.parse import urljoin

from tools.fetcher import AsyncFetcherProtocol
from tools.parser import ParserProtocol
from tools.renderers.course_info import CourseInfoGeneratorRenderer
from tools.urls import Endpoints
from tools.workspace import WorkspaceProtocol


class CLI:
    def __init__(
        self,
        *,
        workspace: WorkspaceProtocol,
        fetcher: AsyncFetcherProtocol,
        parser: ParserProtocol,
        course_info_generator: CourseInfoGeneratorRenderer,
    ) -> None:
        self._workspace = workspace
        self._fetcher = fetcher
        self._parser = parser
        self._course_info_generator = course_info_generator

    async def sync_course(self, course_id: int) -> str:
        info = await self._get_course_info(course_id)
        name = info["title"]
        readme_content = self._course_info_generator.render(info)
        dir_path = self._workspace.create_course_dir(name, readme_content)

        return dir_path

    async def _get_course_info(self, course_id: int) -> dict[str, typing.Any]:
        return self._parser.extract_object(
            await self._fetcher.get(urljoin(Endpoints.courses, f"{course_id}"))
        )
