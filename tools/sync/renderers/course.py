import copy
import typing

import jinja2

from ..cleaner import CleanerProtocol


class CourseRendererProtocol(typing.Protocol):
    def render(self, course: typing.Mapping[str, typing.Any]) -> str:
        pass


class CourseRendered:
    def __init__(
        self,
        template: jinja2.Template,
        sanitizer: CleanerProtocol,
    ) -> None:
        self._template = template
        self._sanitizer = sanitizer

    def render(self, course: typing.Mapping[str, typing.Any]) -> str:
        context = dict(copy.deepcopy(course))
        context["description"] = self._sanitizer.clean(context["description"])
        return self._template.render(context)
