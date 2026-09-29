import yt_dlp

from src.constant import YOUTUBE_URL_PREFIX
from src.format_info_container import FormatContainer
from src.models.format_info import Format

VALID_EXTENSIONS = ["mp4", "m4a", "webm", "mp3"]


def create_youtube_url(video_info: dict):
    return f'{YOUTUBE_URL_PREFIX}{video_info["video_id"]}'


def get_formats(url: str):
    opts = {
        # TODO cookies must be paramatrized
        "cookiesfrombrowser": ("firefox",),
        "js_runtimes": {
            # TODO must use deno lib
            "deno": {
                "path": "/home/bagdad/.deno/bin/deno"
            }
        },
        "remote_components": ["ejs:github"],
        "quiet": False,
        "skip_download": True,
    }

    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=False)

    format_infos = []
    for format_info in info['formats']:
        if format_info.get('filesize', None) is None:
            continue

        if format_info['ext'] in VALID_EXTENSIONS:
            format_infos.append(Format.create_from_dict(format_info))

    return FormatContainer.create_sorted(format_infos)