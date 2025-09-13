import re
import typing


class CleanerProtocol(typing.Protocol):
    def clean(self, string: str) -> str:
        pass


class FilenameCleaner:
    def __init__(self, repl: str = " ") -> None:
        self._repl = repl
        self._symbols_pattern = re.compile(r'[<>:"/\\|?*]')
        self._space_pattern = re.compile(r"\s+")

    def clean(self, string: str) -> str:
        filename = self._symbols_pattern.sub(self._repl, string)
        filename = self._space_pattern.sub(" ", filename)
        filename = filename.strip()
        return filename


class HTMLCleaner:
    def __init__(self, repl: str = "") -> None:
        self._repl = repl
        self._pattern = re.compile(r"<[^<]+?>")

    def clean(self, string: str) -> str:
        text = self._pattern.sub(self._repl, string).strip()
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        return "\n".join(line for line in lines if line)
