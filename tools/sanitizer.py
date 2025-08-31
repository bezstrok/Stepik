import re
import typing


class SanitizerProtocol(typing.Protocol):
    def __call__(self, string: str) -> str:
        pass


class Sanitizer:
    def __init__(self, repl: str = " ") -> None:
        self._repl = repl
        self._pattern = re.compile(r'[<>:"/\\|?*]')

    def __call__(self, string: str) -> str:
        return self._pattern.sub(self._repl, string)
