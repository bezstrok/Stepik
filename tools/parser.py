import typing


class ParserProtocol:
    def extract_object(self, data: typing.Any) -> dict[str, typing.Any]:
        pass

    def extract_objects(self, data: typing.Any) -> list[dict[str, typing.Any]]:
        pass

    def extract_objects_from_list(self, data_list: typing.Iterable[typing.Any]) -> list[dict[str, typing.Any]]:
        pass


# noinspection PyMethodMayBeStatic
class Parser:
    def extract_object(self, data: typing.Any) -> dict[str, typing.Any]:
        return self.extract_objects(data)[0]

    def extract_objects(self, data: typing.Any) -> list[dict[str, typing.Any]]:
        if not isinstance(data, typing.Mapping):
            raise TypeError(f"Expected mapping, got {type(data)}")
        key = next(iter(d for d in data if d != 'meta'))
        return list(map(dict, data[key]))

    def extract_objects_from_list(self, data_list: typing.Iterable[typing.Any]) -> list[dict[str, typing.Any]]:
        data_list = list(data_list)
        if not data_list:
            return []
        if not all(isinstance(data, typing.Mapping) for data in data_list):
            raise TypeError(f"Expected list of mappings, got {type(data_list[0])}")
        key = next(iter(d for d in data_list[0] if d != 'meta'))
        objects: list[dict[str, typing.Any]] = []
        for data in data_list:
            objects.extend(data[key])
        return objects
