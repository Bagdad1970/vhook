import re
from collections.abc import Iterator, Sequence
from operator import attrgetter


class FormatInfoContainer(Sequence):
    VALID_CHOSEN_FORMATS_PATTERN = re.compile(r"^\d+(\+\d+)*$")

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


    @staticmethod
    def _normalize(formats: str):
        return formats.strip().replace(" ", "")


    def _is_chosen_formats_valid(self, chosen_formats: str = ""):
        normalized_chosen_formats = self._normalize(chosen_formats)
        if not re.match(self.VALID_CHOSEN_FORMATS_PATTERN, normalized_chosen_formats):
            return False

        unique_format_nums = set(normalized_chosen_formats.split("+"))

        return all(0 < int(n) <= len(self) for n in unique_format_nums)


    def get_format_ids(self, formats: str = ""):
        normalized_formats = self._normalize(formats)
        if not normalized_formats:
            return ''

        if not self._is_chosen_formats_valid(normalized_formats):
            raise ValueError(f"Invalid formats: {formats!r}")

        unique = dict.fromkeys(normalized_formats.split("+"))

        return '+'.join([ self[int(num) - 1].id for num in unique ])

