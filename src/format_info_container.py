from collections.abc import Iterator, Sequence
from operator import attrgetter


class FormatContainer(Sequence):

    def __init__(self, format_infos: list):
        self.format_infos = format_infos

    @classmethod
    def create_sorted(cls, format_infos: list):
        return cls(sorted(format_infos, key=attrgetter('resolution_type', 'filesize_value')))

    def __iter__(self) -> Iterator:
        return iter(self.format_infos)

    def __len__(self) -> int:
        return len(self.format_infos)

    def __getitem__(self, index):
        return self.format_infos[index]

    def print_formats(self):
        for i, format_info in enumerate(self, start=1):
            print(f"{i}) {format_info}")

    def is_chosen_formats_valid(self, chosen_formats: str):
        unique_format_nums = set(chosen_formats.strip().replace(" ", "").split("+"))

        return all([ 0 < int(format) <= len(self) for format in unique_format_nums ])

    def get_format_ids(self, formats: str):
        splitted_format_indexes = formats.strip().replace(" ", "").split("+")

        return '+'.join([ self[int(index) - 1].id for index in splitted_format_indexes ])

