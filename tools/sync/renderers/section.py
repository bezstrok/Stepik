import copy
import typing

import jinja2

from ..cleaner import CleanerProtocol


class SectionRendererProtocol(typing.Protocol):
    def render(self, section: typing.Mapping[str, typing.Any]) -> str:
        pass


class SectionRendered:
    def __init__(
        self,
        template: jinja2.Template,
        sanitizer: CleanerProtocol,
    ) -> None:
        self._template = template
        self._sanitizer = sanitizer

    def render(self, section: typing.Mapping[str, typing.Any]) -> str:
        context = dict(copy.deepcopy(section))
        context["description"] = self._sanitizer.clean(context["description"])
        return self._template.render(context)
