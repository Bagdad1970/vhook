import re
from dataclasses import dataclass
from enum import IntEnum


class FormatResolutionType(IntEnum):
    AUDIO = 1
    VIDEO = 2


@dataclass()
class Format:
    VIDEO_RESOLUTION_PATTERN = re.compile(r"^(\d+)x(\d+)$")
    AUDIO_RESOLUTION_PATTERN = "audio"

    id: str
    extension: str
    resolution: str
    resolution_type: FormatResolutionType
    filesize: str
    filesize_value: int

    @classmethod
    def create_from_dict(cls, info):
        """Use to create instance from yt-dlp dict"""

        return cls(
            id=info["format_id"],
            extension=info["ext"],
            resolution=info["resolution"],
            resolution_type=cls.get_resolution_type(resolution=info["resolution"], extension=info["ext"]),
            filesize=cls.format_bytes(info.get('filesize')),
            filesize_value=int(info["filesize"]),
        )


    @classmethod
    def get_resolution_type(cls, resolution: str, extension: str) -> FormatResolutionType | None:
        extension = extension.strip().lower()

        if extension == 'm4a':
            return FormatResolutionType.AUDIO

        if extension == 'mp4':
            return FormatResolutionType.VIDEO

        resolution = resolution.strip().lower()
        if re.search(cls.VIDEO_RESOLUTION_PATTERN, resolution):
            return FormatResolutionType.VIDEO

        elif cls.AUDIO_RESOLUTION_PATTERN in resolution:
            return FormatResolutionType.AUDIO

        return None


    @staticmethod
    def format_bytes(size):
        try:
            size = float(size)
        except (TypeError, ValueError):
            raise ValueError(f"Cannot be converted to a number: {size!r}")

        units = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]

        if size == 0:
            return "0 B"

        size = abs(size)
        power = 0
        while size >= 1024 and power < len(units) - 1:
            size /= 1024
            power += 1

        if power == 0:
            result = f"{int(size)} {units[power]}"
        else:
            result = f"{size:.2f} {units[power]}"

        return result
