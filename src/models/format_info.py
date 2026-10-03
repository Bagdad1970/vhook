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
    AUDIO_EXTENSIONS = [ 'mp3', 'm4a' ]
    VIDEO_EXTENSIONS = [ 'mp4' ]

    id: str
    extension: str
    resolution: str
    resolution_type: FormatResolutionType
    filesize: str
    filesize_value: int

    @classmethod
    def create_from_dict(cls, info: dict):
        """Use to create instance from yt-dlp dict"""

        return cls(
            id=info["format_id"],
            extension=info["ext"],
            resolution=info["resolution"],
            resolution_type=cls.get_resolution_type(vcodec=info["vcodec"], acodec=info["acodec"]),
            filesize=cls.format_bytes(info.get('filesize')),
            filesize_value=int(info["filesize"]),
        )


    def is_valid(self):
        return (
            self.id is not None
            and self.extension is not None
            and self.resolution is not None
            and self.resolution_type is not None
            and self.filesize_value > 0
        )


    @classmethod
    def get_resolution_type(cls, vcodec: str | None, acodec: str | None) -> FormatResolutionType | None:
        has_video = vcodec not in [ None, "none" ]
        has_audio = acodec not in [ None, "none" ]

        if has_video and not has_audio:
            return FormatResolutionType.VIDEO
        if has_audio and not has_video:
            return FormatResolutionType.AUDIO

        return None


    @staticmethod
    def format_bytes(bytes_size) -> str:
        try:
            bytes_size = float(bytes_size)
        except (TypeError, ValueError):
            raise ValueError(f"Cannot be converted to a number: {bytes_size!r}")

        if bytes_size < 0:
            raise ValueError("Not enough bytes to format")

        elif bytes_size == 0:
            return "0 B"

        units = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]

        power = 0
        while bytes_size >= 1024 and power < len(units) - 1:
            bytes_size /= 1024
            power += 1

        if power == 0:
            result = f"{int(bytes_size)} {units[power]}"
        else:
            result = f"{bytes_size:.2f} {units[power]}"

        return result
