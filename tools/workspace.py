import pathlib
import typing

from tools.cleaner import CleanerProtocol


class WorkspaceProtocol(typing.Protocol):
    def create_course_dir(self, name: str, readme_content: str) -> str:
        pass

    def create_section_dir(
        self, course_path: str, name: str, readme_content: str
    ) -> str:
        pass


class Workspace:
    def __init__(self, path: str, filename_cleaner: CleanerProtocol) -> None:
        self._path = path
        self._filename_cleaner = filename_cleaner

    def create_course_dir(self, name: str, readme_content: str) -> str:
        name = self._filename_cleaner.clean(name)
        course_path = pathlib.Path(self._path) / name
        course_path.mkdir(exist_ok=True)
        readme_path = course_path / "README.md"
        readme_path.write_text(readme_content)
        return str(course_path)

    def create_section_dir(
        self, course_path: str, name: str, readme_content: str
    ) -> str:
        name = self._filename_cleaner.clean(name)
        section_path = pathlib.Path(course_path) / name
        section_path.mkdir(exist_ok=True)
        readme_path = section_path / "README.md"
        readme_path.write_text(readme_content)
        return str(section_path)
