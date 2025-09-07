import re
import typing


class CleanerProtocol(typing.Protocol):
    def clean(self, string: str) -> str:
        pass


class FilenameCleaner:
    def __init__(self, repl: str = " ") -> None:
        self._repl = repl
        self._pattern = re.compile(r'[<>:"/\\|?*]')

    def clean(self, string: str) -> str:
        return self._pattern.sub(self._repl, string)


class HTMLCleaner:
    def __init__(self, repl: str = "") -> None:
        self._repl = repl
        self._pattern = re.compile(r"<[^<]+?>")

    def clean(self, string: str) -> str:
        clean_text = self._pattern.sub(self._repl, string).strip()
        lines = [line.strip() for line in clean_text.splitlines() if line.strip()]
        return "\n".join(line for line in lines if line)
