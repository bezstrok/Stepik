import typing
from urllib.parse import urljoin

from tools.fetcher import AsyncFetcherProtocol
from tools.parser import ParserProtocol
from tools.renderers.course import CourseRendererProtocol
from tools.renderers.section import SectionRendererProtocol
from tools.urls import Endpoints
from tools.workspace import WorkspaceProtocol


class CLI:
    def __init__(
        self,
        *,
        workspace: WorkspaceProtocol,
        fetcher: AsyncFetcherProtocol,
        parser: ParserProtocol,
        course_generator: CourseRendererProtocol,
        section_generator: SectionRendererProtocol,
    ) -> None:
        self._workspace = workspace
        self._fetcher = fetcher
        self._parser = parser
        self._course_generator = course_generator
        self._section_generator = section_generator

    async def sync_course(self, course_id: int) -> str:
        course = await self._get_course(course_id)
        self._save_course(course)

        sections = await self._get_sections(course["sections"])
        for section in sections:
            self._save_section(section)

    def _save_section(
        self, course_path: str, section: typing.Mapping[str, typing.Any]
    ) -> str:
        name = section["title"]
        readme_content = self._section_generator.render(section)
        section_path = self._workspace.create_section_dir(
            course_path, name, readme_content
        )
        return section_path

    def _save_course(self, course: typing.Mapping[str, typing.Any]) -> str:
        name = course["title"]
        readme_content = self._course_generator.render(course)
        course_path = self._workspace.create_course_dir(name, readme_content)
        return course_path

    async def _get_course(self, course_id: int) -> dict[str, typing.Any]:
        return self._parser.extract_object(
            await self._fetcher.get(urljoin(Endpoints.courses, f"{course_id}"))
        )

    async def _get_sections(
        self, section_ids: typing.Iterable[int]
    ) -> list[dict[str, typing.Any]]:
        return self._parser.extract_objects_from_iterable(
            await self._fetcher.get_paginated(
                Endpoints.sections,
                params={"ids": list(section_ids)},
            )
        )
