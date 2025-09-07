import copy
import typing

import jinja2

from tools.cleaner import CleanerProtocol


class CourseInfoGeneratorRenderer(typing.Protocol):
    def render(self, course_info: dict[str, typing.Any]) -> str:
        pass


class CourseInfoRendered:
    def __init__(
        self,
        template: jinja2.Template,
        sanitizer: CleanerProtocol,
    ) -> None:
        self._template = template
        self._sanitizer = sanitizer

    def render(self, course_info: dict[str, typing.Any]) -> str:
        context = copy.deepcopy(course_info)
        context["description"] = self._sanitizer.clean(context["description"])
        return self._template.render(context)
