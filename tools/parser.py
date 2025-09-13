import typing


class ParserProtocol(typing.Protocol):
    def extract_object(self, data: typing.Any) -> dict[str, typing.Any]:
        pass

    def extract_objects(self, data: typing.Any) -> list[dict[str, typing.Any]]:
        pass

    def extract_objects_from_iterable(
        self, it: typing.Iterable[typing.Any]
    ) -> list[dict[str, typing.Any]]:
        pass


# noinspection PyMethodMayBeStatic
class Parser:
    def extract_object(self, data: typing.Any) -> dict[str, typing.Any]:
        return self.extract_objects(data)[0]

    def extract_objects(self, data: typing.Any) -> list[dict[str, typing.Any]]:
        if not isinstance(data, typing.Mapping):
            raise TypeError(f"Expected mapping, got {type(data)}")
        key = next(iter(d for d in data if d != "meta"))
        return list(map(dict, data[key]))

    def extract_objects_from_iterable(
        self, it: typing.Iterable[typing.Any]
    ) -> list[dict[str, typing.Any]]:
        list_data = list(it)
        if not list_data:
            return []
        if not all(isinstance(data, typing.Mapping) for data in list_data):
            raise TypeError(f"Expected list of mappings, got {type(list_data[0])}")
        key = next(iter(d for d in list_data[0] if d != "meta"))
        objects: list[dict[str, typing.Any]] = []
        for list_data in list_data:
            objects.extend(list_data[key])
        return objects
